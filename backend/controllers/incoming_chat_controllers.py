from chat_interfaces.telegram import TelegramInterface, ChatInterfaceError
from controllers.types.telegram_models import TelegramUpdate
from core.logger import get_logger

logger = get_logger(__name__)


class IncomingChatController:

    def handle_telegram_update(self, telegram_interface: TelegramInterface, update: TelegramUpdate):
        try:
            event = telegram_interface.to_incoming_event(update)
            logger.info(
                "Received chat event: interface=%s, user=%s, conversation=%s, message=%r",
                event.chat_interface,
                event.user_external_id,
                event.conversation_id,
                event.message,
            )

            # Echo the message back so the bot confirms it's listening
            if event.message:
                telegram_interface.send_message(
                    chat_id=int(event.conversation_id),
                    text=f"Got your message: {event.message}",
                )

        except ChatInterfaceError:
            logger.exception("Chat interface error while handling telegram update")
        except Exception:
            logger.exception("Error while handling telegram update")
            raise