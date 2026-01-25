from fastapi import APIRouter, Request, Response
from controllers.types.telegram_models import TelegramUpdate 

from controllers.incoming_chat_controllers import IncomingChatController
from chat_interfaces.telegram import TelegramInterface
from constants.routes_contants import TELEGRAM_WEBHOOK

router = APIRouter()




@router.post(TELEGRAM_WEBHOOK)
async def telegram_webhook_handler(request: Request):
    raw_payload = await request.json()
    telegram_interface = TelegramInterface()
    incoming_chat_controller = IncomingChatController()

    try:
        update = TelegramUpdate.model_validate(raw_payload)
    except Exception:
        # malformed payload — ignore safely
        return Response(status_code=200)

    if not update.message:
        return Response(status_code=200)

    incoming_chat_controller.handle_telegram_update(
        telegram_interface=telegram_interface,
        update=update,
    )

    return Response(status_code=200)
