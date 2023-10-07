from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseMeta(BaseModel):
    source: str = Field(description="service name (queue)")
    reply_to: str | None = Field(
        description="reply to queue name, if no reply None"
    )
    service: str = Field(description="another service name")
    action: str = Field(..., description="another service action name")
    sent_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="sent at (datetime with tz)",
    )
    message_uuid: UUID = Field(
        default_factory=uuid4, description="uuid4 of this message"
    )
    reply_to_message_uuid: UUID | None = Field(
        None,
        description="uuid4 reply message, if first message then None",
    )
    path: list[str] = Field(
        default_factory=list, description="message reply history"
    )


class RequestMeta(BaseMeta):
    reply_to: str
    service: str
    reply_to_message_uuid: UUID | None = None


class ResponseMeta(BaseMeta):
    reply_to: str | None = None


class RequestMessageBase(BaseModel):
    meta: RequestMeta
    payload: dict | None = None


class MessageBase(BaseModel):
    meta: BaseMeta
    payload: BaseModel
