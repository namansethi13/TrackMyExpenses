from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from auth.jwt_service import verify_access_token

# Paths that do not require authentication
UNAUTHENTICATED_PATHS = ["/webhooks/", "/auth/"]


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(p) for p in UNAUTHENTICATED_PATHS):
            return await call_next(request)

        header = request.headers.get("Authorization")
        if not header or not header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})

        token = header.split(" ")[1]
        payload = verify_access_token(token)
        if not payload:
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})

        request.state.user = payload
        return await call_next(request)
