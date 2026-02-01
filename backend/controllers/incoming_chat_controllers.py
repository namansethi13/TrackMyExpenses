from core.logger import get_logger

logger = get_logger(__name__)

class IncomingChatController:
    # Implement the logic to handle incoming chat messages
    def handle_telegram_update(self, telegram_interface, update):
        try:
            chat_id = update.message.chat.id
            logger.info("Handling telegram update for chat_id=%s", chat_id)

            # TODO: call into services / business logic here
        except Exception:
            logger.exception("Error while handling telegram update")
            raise