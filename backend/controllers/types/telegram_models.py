from pydantic import BaseModel, Field
from typing import Optional


class TelegramUser(BaseModel):
    id: int


class TelegramChat(BaseModel):
    id: int


class TelegramMessage(BaseModel):
    message_id: int
    date: int
    text: Optional[str] = None
    from_: TelegramUser = Field(alias="from")
    chat: TelegramChat

    model_config = {"populate_by_name": True}


class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] = None
