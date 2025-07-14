from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True 