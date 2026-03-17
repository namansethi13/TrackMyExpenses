import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from core.logger import get_logger

logger = get_logger(__name__)

_SECRET = os.getenv("JWT_SECRET", "")
_ALGORITHM = "HS256"
_EXPIRE_DAYS = 10


def create_access_token(uid: str, phone: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=_EXPIRE_DAYS)
    payload = {"sub": uid, "phone": phone, "exp": expire}
    return jwt.encode(payload, _SECRET, algorithm=_ALGORITHM)


def verify_access_token(token: str) -> dict | None:
    """
    Returns decoded payload if valid, None otherwise.
    Logs reason for failure to aid debugging.
    """
    try:
        return jwt.decode(token, _SECRET, algorithms=[_ALGORITHM])
    except ExpiredSignatureError:
        logger.debug("JWT expired")
    except InvalidTokenError as e:
        logger.debug("JWT invalid: %s", e)
    return None
