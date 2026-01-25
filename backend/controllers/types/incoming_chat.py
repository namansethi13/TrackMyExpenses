from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class ChatInterfaceType(str, Enum):
    TELEGRAM = "Telegram"


class IncomingChatEvent(BaseModel):
    event_id: str = Field(..., description="Unique identifier for the chat event")
    chat_interface: ChatInterfaceType = Field(..., description="Type of chat interface (e.g., Telegram, WhatsApp)")
    message: Optional[str] = Field(None, description="Content of the incoming chat message")
    timestamp: int = Field(..., description="Timestamp of when the message was received")
    user_external_id: str = Field(..., description="External identifier for the user in the chat interface")
    conversation_id : str = Field(..., description="Identifier for the conversation thread")
    raw_payload: Optional[dict] = Field(None, description="Raw payload received from the chat interface")