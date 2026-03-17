"""
Telegram chat interface module.

Converts incoming Telegram webhook payloads into IncomingChatEvent.
"""

import os
from uuid import uuid4
from typing import Optional
import requests

from controllers.types.incoming_chat import (
    IncomingChatEvent,
    ChatInterfaceType,
)

from chat_interfaces.base_chat_interface import BaseChatInterface
from controllers.types.telegram_models import TelegramUpdate
from core.logger import get_logger

logger = get_logger(__name__)

class ChatInterfaceError(Exception):
    """Custom exception for chat interface errors."""
    pass


class TelegramInterface(BaseChatInterface):

    TELEGRAM_API_URL = "https://api.telegram.org"

    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")

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

    def _validate_response(self, response_data: dict) -> True:
        """
        Validate Telegram API response.
        
        Args:
            response_data (dict): The JSON response from Telegram API
        
        Returns:
            True if response is valid
        
        Raises:
            ChatInterfaceError: If response indicates an error
        """
        if not response_data.get("ok"):
            error_msg = response_data.get("description", "Unknown error")
            error_code = response_data.get("error_code", "N/A")
            raise ChatInterfaceError(
                f"Telegram API error (code {error_code}): {error_msg}"
            )
        return True

    def send_message(self, chat_id: int, text: str) -> bool:
        """
        Send a message to a Telegram chat.

        Args:
            chat_id (int): The Telegram chat ID to send the message to
            text (str): The message text

        Returns:
            bool: True if message was sent successfully

        Raises:
            ChatInterfaceError: If the API call fails
        """
        try:
            api_url = f"{self.TELEGRAM_API_URL}/bot{self.bot_token}/sendMessage"
            response = requests.post(api_url, json={"chat_id": chat_id, "text": text}, timeout=10)
            response.raise_for_status()
            self._validate_response(response.json())
            return True
        except ChatInterfaceError:
            raise
        except requests.exceptions.RequestException as e:
            raise ChatInterfaceError(f"Failed to send Telegram message: {e}") from e
        except Exception as e:
            raise ChatInterfaceError(f"Unexpected error sending Telegram message: {e}") from e

    def setWebhook(self, webhook_url: str) -> bool:
        """
        Set the Telegram bot webhook URL.

        Args:
            webhook_url (str): The public webhook URL where Telegram should send updates

        Returns:
            bool: True if webhook was set successfully, False otherwise

        Raises:
            ChatInterfaceError: If API validation fails
        """
        try:
            # Build the API endpoint URL
            api_url = f"{self.TELEGRAM_API_URL}/bot{self.bot_token}/setWebhook"
            
            payload = {
                "url": webhook_url,
                "allowed_updates": ["message"],  # Only listen to message updates
            }
            
            response = requests.post(api_url, json=payload, timeout=10)
            response.raise_for_status()
            
            response_data = response.json()
            
            # Validate the response
            self._validate_response(response_data)
            
            logger.info(f"Telegram webhook set successfully to: {webhook_url}")
            return True
                
        except ChatInterfaceError as e:
            logger.error(f"Telegram API validation error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to set Telegram webhook: {e}"
            logger.error(error_msg)
            raise ChatInterfaceError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error setting Telegram webhook: {e}"
            logger.error(error_msg)
            raise ChatInterfaceError(error_msg) from e
