import json
import logging
import traceback
import uuid
from datetime import datetime
from json.encoder import JSONEncoder
from typing import Any, Literal

import pytz
from pydantic import BaseModel

from aioka.server.errors.schema import ExceptionSchema
from aioka.server.schema import BaseMeta

logger = logging.getLogger(__name__)


def create_message(meta: dict, payload: dict):
    return {
        "meta": meta,
        "payload": payload,
    }


def create_error_response_meta(service_name: str):
    return {
        "from": service_name,
        "reply_to": None,
        "sent_at": datetime.now(tz=pytz.utc),
        "message_uuid": uuid.uuid4(),
        "reply_to_message_uuid": None,
    }


class JsonEncoder(JSONEncoder):
    # fixme мне кажется где-то я этот клас уже видел в таком исполнении
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, uuid.UUID):
            return str(o)
        return super().default(o)


def gen_error_message(
    raw_message,
    e,
    error_type: Literal["internal", "validation"] = "validation",
):
    if error_type == "validation":
        if hasattr(e, "errors") and callable(e.errors):
            details = e.errors()
        else:
            details = []

        error = generate_error(
            error_type=error_type,
            validation_details={
                "error": str(e),
                "trace": traceback.format_exc(),
                "details": details,
            },
            raw_message=raw_message,
        )
    else:
        error = generate_error(
            error_type=error_type,
            internal_details={
                "error": str(e),
                "trace": traceback.format_exc(),
            },
            raw_message=raw_message,
        )

    meta_response = create_error_response_meta()

    error_message = json.dumps(
        create_message(meta_response, error.model_dump(by_alias=True)),
        indent=2,
        ensure_ascii=False,
        cls=JsonEncoder,
    ).encode()

    return error_message


def generate_meta(meta: BaseModel | dict, service_name: str) -> BaseMeta:
    if isinstance(meta, BaseModel):
        meta_dict: dict = meta.model_dump(by_alias=True)
    else:
        meta_dict = meta
    return BaseMeta.model_validate(
        {
            **meta_dict,
            "from": service_name,
            "reply_to": None,
            "sent_at": datetime.now(tz=pytz.utc),
            "message_uuid": str(uuid.uuid4()),
            "reply_to_message_uuid": meta_dict.get("message_uuid"),
        }
    )


def generate_error(
    raw_message: str = None,
    response_ok: bool = True,
    error_type: Literal["internal", "validation"] = "internal",
    validation_details=None,
    internal_details=None,
) -> ExceptionSchema:
    if validation_details is None:
        validation_details = {}
    if internal_details is None:
        internal_details = {}

    return ExceptionSchema.model_validate(
        {
            "response_ok": response_ok,
            "error_type": error_type,
            "validation_details": validation_details,
            "internal_details": internal_details,
            "raw_message": raw_message,
        }
    )
