from typing import Literal, TypeAlias

from pydantic import BaseModel, Field

from aioka.server.schema import BaseMeta

ErrorTypes: TypeAlias = Literal["validation", "internal"]


class ExceptionSchema(BaseModel):
    response_ok: bool = Field(description="True если запрос обработан успешно")
    error_type: ErrorTypes = Field(description="Тип ошибки")
    validation_details: dict = Field(
        {}, description="Детали для ошибки валидации"
    )
    internal_details: dict = Field({}, description="Детали для других ошибок")
    raw_message: str | None = Field(
        None,
        description="Сообщение, которое не удалось обработать (для rmq)",
    )


class FullErrorSchema(BaseModel):
    meta: BaseMeta
    payload: ExceptionSchema
