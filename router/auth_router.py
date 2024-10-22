from fastapi import APIRouter, Body, Depends, Form, Request
from fastapi_limiter.depends import RateLimiter

from config.env import Env
from core.exceptions.http import CustomHttpException
from core.logging import logger
from domain.rest import auth_rest, generic_resp
from service import auth_service
from utils import aes as aes_utils

AuthRouter = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@AuthRouter.post(
    "/login/dev",
    dependencies=[Depends(RateLimiter(times=20, seconds=60))],
    description="""
    username and password required (unencrypted).
    only accept x-www-form-urlencoded.
    used for development which require for swagger ui authentication.
    return 403 if in production.
""",
)
def login_dev(
    username: str = Form(...),
    password: str = Form(...),
    auth_service: auth_service.AuthService = Depends(),
):
    if Env.PRODUCTION:
        raise CustomHttpException(
            status_code=403,
            message="forbidden",
        )

    resp = auth_service.login(username=username, password=password)
    return resp


@AuthRouter.post(
    "/login",
    response_model=auth_rest.LoginResp,
    dependencies=[Depends(RateLimiter(times=20, seconds=60))],
    description="""
    username and password are required.
    accept x-www-form-urlencoded and json.
    username and password must be encrypted in aes256.
""",
)
def login(
    request: Request,
    body=Body(),
    auth_service: auth_service.AuthService = Depends(),
):
    """
    manually decode the body
    because fastapi oauth2 schema doesn't support json (only urlencoded form)
    and client need it in json
    """
    content_type = request.headers.get("Content-Type")
    payload = {}
    if content_type == "application/x-www-form-urlencoded":
        body: str = body.decode("utf-8")
        splits = body.split("&")
        for split in splits:
            key, value = split.split("=")
            payload[key] = value
    elif content_type == "application/json":
        payload = body

    if "username" not in payload and "password" not in payload:
        exc = CustomHttpException(
            status_code=400,
            message="username and password are required",
        )
        logger.error(exc)
        raise exc

    logger.debug(f"payload: {payload}")
    try:
        username = aes_utils.decrypt(payload["username"])
        password = aes_utils.decrypt(payload["password"])
    except Exception as e:
        logger.error(e)
        raise CustomHttpException(
            status_code=400,
            message="invalid encryption",
        )

    resp = auth_service.login(
        username=username,
        password=password,
    )

    return resp
