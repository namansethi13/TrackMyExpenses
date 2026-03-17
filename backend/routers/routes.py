from fastapi import APIRouter, HTTPException, Request, Response

from controllers.auth_controller import AuthController
from controllers.types.auth_models import ExchangeRequest, TokenResponse
from controllers.types.telegram_models import TelegramUpdate
from controllers.incoming_chat_controllers import IncomingChatController
from chat_interfaces.telegram import TelegramInterface
from constants.routes_contants import AUTH_EXCHANGE, TELEGRAM_WEBHOOK
from core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post(AUTH_EXCHANGE, response_model=TokenResponse)
async def auth_exchange(body: ExchangeRequest):
    try:
        return AuthController().exchange_token(body)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired Firebase token")




@router.post(TELEGRAM_WEBHOOK)
async def telegram_webhook_handler(request: Request):
    raw_payload = await request.json()
    logger.debug("Received raw telegram payload: %s", raw_payload)
    telegram_interface = TelegramInterface()
    incoming_chat_controller = IncomingChatController()

    try:
        update = TelegramUpdate.model_validate(raw_payload)
    except Exception:
        # malformed payload — ignore safely
        logger.exception("Malformed payload in telegram webhook")
        return Response(status_code=200)

    if not update.message:
        logger.debug("Telegram update has no message; ignoring")
        return Response(status_code=200)

    logger.info("Receiving telegram update: chat=%s, message_id=%s",
                update.message.chat.id,
                update.message.message_id)

    incoming_chat_controller.handle_telegram_update(
        telegram_interface=telegram_interface,
        update=update,
    )

    return Response(status_code=200)
