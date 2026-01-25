from pydantic import BaseModel
from typing import Optional, Dict, Any


class TelegramUser(BaseModel):
    id: int


class TelegramChat(BaseModel):
    id: int


class TelegramMessage(BaseModel):
    message_id: int
    date: int
    text: Optional[str]
    from_: TelegramUser
    chat: TelegramChat

    class Config:
        fields = {
            "from_": "from"
        }
    
class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] = None
