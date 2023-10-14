from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str


class TokenCreate(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    status: bool
    created_at: datetime


class TokenData(BaseModel):
    id: int
