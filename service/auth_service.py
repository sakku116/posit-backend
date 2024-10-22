from datetime import datetime, timedelta

from fastapi import Depends
from jwt import exceptions as jwt_exceptions

from config.env import Env
from core.exceptions.http import CustomHttpException
from core.logging import logger
from domain.dto import auth_dto
from domain.model import session_model, user_model
from domain.rest import auth_rest
from repository import session_repo, user_repo
from utils import bcrypt as bcrypt_utils
from utils import helper
from utils import jwt as jwt_utils


class AuthService:
    def __init__(
        self,
        user_repo: user_repo.UserRepo = Depends(),
        session_repo: session_repo.SessionRepo = Depends(),
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo

    def login(self, username: str, password: str) -> auth_rest.LoginResp:
        # check username existance
        user = self.user_repo.get(username=username)
        if not user:
            exc = CustomHttpException(
                status_code=401,
                message="Invalid username",
            )
            logger.error(exc)
            raise exc

        # check if user banned
        if user.banned:
            exc = CustomHttpException(
                status_code=403,
                message="User banned",
            )
            logger.error(exc)
            raise exc

        # check password
        is_pw_match = bcrypt_utils.checkPassword(password, user.password)
        if is_pw_match:
            exc = CustomHttpException(
                status_code=401,
                message="Invalid password",
            )
            logger.error(exc)
            raise exc

        # generate jwt token
        session_id = helper.generateUUID()
        session_exp = datetime.utcnow() + timedelta(hours=Env.JWT_EXP)
        jwt_token = jwt_utils.encodeToken(
            auth_dto.JWTPayload(
                sub=user.id,
                username=user.username,
                fullname=user.fullname,
                email=user.email,
                banned=user.banned,
                session_id=session_id,
                exp=session_exp,
            ).model_dump(),
            Env.JWT_SECRET,
        )

        # create session
        time_now = helper.timeNowEpoch()
        new_session = session_model.SessionModel(
            id=session_id,
            created_at=time_now,
            updated_at=time_now,
            created_by=user.id,
            jwt_token=jwt_token,
            expired_at=int(session_exp.timestamp()),
        )
        self.session_repo.create(session=new_session)

        # update user last_active
        user.last_active = time_now
        self.user_repo.update(id=user.id, data=user)

        result = auth_rest.LoginResp(
            access_token=jwt_token,
        )

        return result

    def verifyToken(self, token: str = None) -> auth_dto.CurrentUser:
        # find session
        session_token = token.removeprefix("Bearer ")
        session = self.session_repo.get(id=session_token)
        if not session:
            exc = CustomHttpException(
                status_code=401,
                message="session token not found",
            )
            logger.error(exc)
            raise exc

        # decode token
        claims = {}
        try:
            claims = jwt_utils.decodeToken(session.jwt_token, Env.JWT_SECRET)
            claims = auth_dto.JWTPayload(**claims)
        except jwt_exceptions.ExpiredSignatureError as e:
            exc = CustomHttpException(
                status_code=401,
                message="Token expired",
            )
            logger.error(exc)
            raise exc
        except Exception as e:
            exc = CustomHttpException(
                status_code=401,
                message="Invalid token",
            )

        # check user active
        if claims.banned:
            exc = CustomHttpException(
                status_code=403,
                message="User banned",
            )
            logger.error(exc)
            raise exc

        # update last_active
        self.user_repo.patch(
            id=claims.sub, data=user_model.UserModel(last_active=helper.timeNowEpoch())
        )

        result = auth_dto.CurrentUser(
            claims=claims.model_dump(),
        )

        return result
