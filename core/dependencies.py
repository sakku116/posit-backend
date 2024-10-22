from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from config.env import Env
from domain.dto import auth_dto
from service.auth_service import AuthService

reusable_token = OAuth2PasswordBearer(
    "/auth/login" if Env.PRODUCTION else "/auth/login/dev"
)


async def verifyToken(
    auth_service: AuthService = Depends(),
    token: str = Depends(reusable_token),
) -> auth_dto.CurrentUser:
    current_user = auth_service.verifyToken(token=token)
    return current_user
