from pydantic import BaseModel
from typing import Optional

class LoginReq(BaseModel):
    username: str
    password: str

class LoginResp(BaseModel):
    session_token: str
    refresh_token: Optional[str] = None