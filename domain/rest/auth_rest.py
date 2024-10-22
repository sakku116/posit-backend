from pydantic import BaseModel
from typing import Optional
from domain.dto import auth_dto
from domain.rest import generic_resp

class LoginReq(BaseModel):
    username: str
    password: str

class LoginResp(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None

class CheckTokenResp(auth_dto.JWTPayload):
    pass