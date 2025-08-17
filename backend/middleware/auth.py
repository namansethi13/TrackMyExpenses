from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import firebase_admin
from .firebase_config import default_app
from firebase_admin import auth

class AuthMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request : Request, call_next):
        header = request.headers.get("Authorization")
        if not header or not header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        id_token = header.split(" ")[1]
        try:
            decoded_token = auth.verify_id_token(id_token)
            if decoded_token:
                request.state.user = decoded_token
            else:
                return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        except Exception as e:
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        return await call_next(request)
