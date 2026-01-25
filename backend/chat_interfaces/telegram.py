"""
Telegram chat interface module.

Converts incoming Telegram webhook payloads into IncomingChatEvent.
"""

from uuid import uuid4
from typing import Optional

from controllers.types.incoming_chat import (
    IncomingChatEvent,
    ChatInterfaceType,
)

from chat_interfaces.base_chat_interface import BaseChatInterface
from controllers.types.telegram_models import TelegramUpdate

class ChatInterfaceError(Exception):
    """Custom exception for chat interface errors."""
    pass


class TelegramInterface(BaseChatInterface):

    def to_incoming_event(self, payload: TelegramUpdate) -> Optional[IncomingChatEvent]:
        """
        Convert Telegram webhook (with message) payload to IncomingChatEvent.
        Assumes payload is a valid Telegram update with a message.
        Args:
            payload (TelegramUpdate): The incoming Telegram webhook payload.
        """

        message = payload.message
        if not message:
            raise ChatInterfaceError("Unsupported Telegram update type")

        return IncomingChatEvent(
            event_id=str(uuid4()),
            chat_interface=ChatInterfaceType.TELEGRAM,
            message=message.text,
            timestamp=message.date,  # Telegram gives unix seconds
            user_external_id=str(message.from_.id),
            conversation_id=str(message.chat.id),
            raw_payload=payload,
        )
