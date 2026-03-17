from pydantic import BaseModel


class ExchangeRequest(BaseModel):
    firebase_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 60 * 60 * 24 * 10  # 10 days in seconds
