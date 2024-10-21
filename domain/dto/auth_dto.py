from pydantic import BaseModel
from domain.model import user_model
from datetime import datetime

class JWTPayload(BaseModel):
    sub: str
    username: str
    fullname: str
    email: str
    banned: bool
    session_id: str
    exp: datetime

class CurrentUser(JWTPayload):
    pass