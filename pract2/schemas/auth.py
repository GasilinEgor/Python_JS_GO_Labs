from pydantic import BaseModel, Field
from datetime import datetime

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime

class RefreshRequest(BaseModel):
    refresh_token: str