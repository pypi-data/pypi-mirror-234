import json
import logging
import uuid
from datetime import datetime
from typing import Literal, Optional, Union

import pytz
from aio_pika import IncomingMessage
from pydantic import BaseModel, ValidationError, create_model

from aioka.server import BaseMeta, MessageBase, RequestMeta, ResponseMeta
from aioka.server.errors.fmt import gen_error_message

from .base import BaseAction

logger = logging.getLogger(__name__)


class Action(BaseAction):
    REQUEST_META = RequestMeta
    REQUEST_PAYLOAD: BaseModel

    RESPONSE_META = ResponseMeta
    RESPONSE_PAYLOAD: BaseModel

    def __init__(self, action_name: str):
        super(Action, self).__init__(action_name=action_name)

        self.REQUEST_META = create_model(
            "REQUEST_META",
            __base__=self.REQUEST_META,
            action=(Literal[self.action_name], ...),
        )
        self.REQUEST_META_VALIDATION = create_model(
            "REQUEST_META_VALIDATION",
            meta=(self.REQUEST_META, ...),
            payload=(Optional[dict], None),
        )

    @property
    def queue_name(self):
        return fmt_queue_name(
            self.action_name, service_name=self._service_name
        )

    @property
    def routing_keys(self):
        return [self.queue_name]

    async def consume(self, message: IncomingMessage):
        async with message.process(
            requeue=True,
            reject_on_redelivered=False,
            ignore_processed=True,
        ):
            # 1) проверяем валидность схемы
            # 1.1) проверяем что пришел json
            try:
                json_data = json.loads(message.body)
            except json.JSONDecodeError as e:
                logger.error("Is not JSON", exc_info=True)
                error_message = gen_error_message(
                    message.body, e, service_name=self.service_name
                )
                await self.publish(message=error_message)
                return
            # 1.2 десериализовать сообщение
            # 1.3 проверить корректность меты c точки зрения общей схемы
            try:
                message_obj = self.REQUEST_META_VALIDATION.model_validate(
                    json_data
                )
                meta_obj = message_obj.meta
                assert isinstance(meta_obj, self.REQUEST_META)

            except ValidationError as e:
                logger.error("Meta is not valid", exc_info=True)
                error_message = gen_error_message(
                    message.body, e, service_name=self.service_name
                )
                await self.publish(message=error_message)
                return
            # 1.4 проверить корректность payload
            try:
                payload_obj = self.REQUEST_PAYLOAD.parse_obj(
                    message_obj.payload
                )
            except ValidationError as e:
                logger.error("Payload is not valid", exc_info=True)
                error_message = gen_error_message(
                    message.body, e, service_name=self.service_name
                )
                await self.publish(message=error_message)
                if meta_obj.reply_to:
                    await self.publish(
                        routing_key=meta_obj.reply_to, message=error_message
                    )
                return
            # Выполнить
            try:
                RESPONSE_TYPE = self.RESPONSE_PAYLOAD
                response: dict | RESPONSE_TYPE | None = await self(
                    meta=meta_obj, payload=payload_obj
                )
                if meta_obj.reply_to and response is not None:
                    await self.publish(
                        routing_key=meta_obj.reply_to,
                        message=RESPONSE_TYPE.model_validate(response),
                    )
            except Exception as e:
                logger.error(
                    f"Unhandled exception in {self.__call__}", exc_info=True
                )
                error_message = gen_error_message(
                    message.body,
                    e,
                    error_type="internal",
                    service_name=self.service_name,
                )
                await self.publish(message=error_message)
                if meta_obj.reply_to:
                    await self.publish(
                        routing_key=meta_obj.reply_to, message=error_message
                    )

    async def validate_message(
        self, body: bytes
    ) -> Union[bool, tuple[BaseModel, BaseModel]]:
        ...

    async def validate_meta(self, body: bytes):
        ...

    async def validate(self, body: bytes):
        ...

    async def consume_success(
        self, meta: BaseMeta, response_payload: BaseModel
    ):
        response_meta = self.RESPONSE_META.model_validate(
            {
                "from": self._service_name,
                "reply_to": None,
                "service": meta.service,
                "action": meta.action,
                "sent_at": datetime.now(tz=pytz.utc),
                "message_uuid": uuid.uuid4(),
                "reply_to_message_uuid": meta.message_uuid,
                "path": meta.path + [self._service_name],
            }
        )
        message = MessageBase(meta=response_meta, payload=response_payload)
        logger.debug(
            f"consume success reply_to: {meta.reply_to}, message: {message}"
        )
        await self.publish(routing_key=meta.reply_to, message=message)

    async def publish(
        self,
        message: Union[BaseModel, bytes],
        routing_key: Optional[str] = None,
    ):
        if isinstance(message, BaseModel):
            message_body = message.model_dump_json(
                indent=2, by_alias=True
            ).encode()
        elif isinstance(message, str):
            message_body = message.encode()
        else:
            message_body = message
        await self.client(
            message=message_body,
            routing_key=routing_key,
        )

    async def __call__(self, meta: BaseMeta, payload: BaseModel):
        raise NotImplementedError


def fmt_queue_name(handle_name: str, service_name: str):
    return f"{service_name}.{handle_name}"
