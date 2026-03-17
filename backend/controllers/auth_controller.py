from firebase_admin import auth as firebase_auth

from auth.jwt_service import create_access_token
from controllers.types.auth_models import ExchangeRequest, TokenResponse
from daos.user_dao import UserDAO
from core.logger import get_logger

logger = get_logger(__name__)


class AuthController:

    def __init__(self):
        self._user_dao = UserDAO()

    def exchange_token(self, request: ExchangeRequest) -> TokenResponse:
        """
        Verify a Firebase ID token, upsert the user in MongoDB,
        and issue a signed JWT for all subsequent API calls.
        """
        try:
            decoded = firebase_auth.verify_id_token(request.firebase_token)
        except Exception:
            logger.exception("Firebase token verification failed")
            raise

        uid: str = decoded["uid"]
        phone: str = decoded.get("phone_number", "")

        self._user_dao.upsert_by_firebase_uid(uid, phone)

        access_token = create_access_token(uid=uid, phone=phone)
        logger.info("Issued access token for uid=%s", uid)

        return TokenResponse(access_token=access_token)
