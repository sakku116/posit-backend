from datetime import datetime, timedelta

from fastapi import Depends

from config.env import Env
from core.exceptions.http import CustomHttpException
from core.logging import logger
from domain.dto import auth_dto
from domain.rest import auth_rest
from domain.model import session_model
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
        if user.password != password:
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
            expired_at=int(session_exp.timestamp())
        )
        self.session_repo.create(session=new_session)

        # update user last_active
        user.last_active = time_now
        self.user_repo.update(id=user.id, data=user)

        return jwt_token