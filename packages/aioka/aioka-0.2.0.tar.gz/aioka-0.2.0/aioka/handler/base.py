from functools import wraps
from typing import AsyncIterable, Awaitable, Callable, Type

from pydantic import BaseModel

from aioka.action.base import BaseAction
from aioka.action.master import Action
from aioka.server import RequestMeta, ResponseMeta
from aioka.server.base import BaseServer


class BaseHandler:
    """
    Basic implementation of the handler.
    Binds actions to rft_proxy calls and initializes the client
    """

    __slots__ = ("routes", "server")

    server: BaseServer

    def __init__(self):
        self.routes: dict[str, Type[BaseAction]] = {}

    def set_server(self, server: BaseServer):
        """
        Фабрика для асинхронного создания инстанса класса

        :param server: Кастомный сервер, базирующейся на BaseServer
        """
        self.server = server
        return self

    async def _bind_procedures(self) -> AsyncIterable:
        for action_name, action_instance in self.routes.items():
            action_instance.service_name = self.server.service_name
            yield action_instance

    async def bind(self):
        """Метод для биндинга процедур к серверу"""
        async for procedure in self._bind_procedures():
            await self.server.bind(procedure.action_name, procedure)

    def add_action(self, action_name: str, action: BaseAction):
        self.routes.update({action_name: action})

    def action(
        self,
        action_name: str,
        request_payload: BaseModel = BaseModel,
        response_payload: BaseModel = BaseModel,
        request_meta: RequestMeta = RequestMeta,
        response_meta: ResponseMeta = ResponseMeta,
        action_class: Type[BaseAction] = Action,
    ):
        def decorator(
            func: Callable[
                [BaseModel, BaseModel],
                Awaitable[BaseModel | dict | list | None],
            ]
        ) -> BaseAction:
            @wraps(func)
            async def wrapper(meta: request_meta, payload: request_payload):
                return await func(meta, payload)

            action = action_class(action_name=action_name)
            action.__call__ = wrapper
            action.REQUEST_PAYLOAD = request_payload
            action.RESPONSE_PAYLOAD = response_payload
            action.REQUEST_META = request_meta
            action.RESPONSE_META = response_meta

            self.add_action(action_name=action_name, action=action)
            return action

        return decorator
