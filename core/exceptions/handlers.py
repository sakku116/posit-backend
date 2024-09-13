from fastapi import Request
from fastapi.responses import JSONResponse

from core.exceptions.http import CustomHttpException
from domain.rest import generic_resp
from fastapi.exceptions import RequestValidationError
from typing import Union


async def customHttpExceptionHandler(request: Request, exc: CustomHttpException):
    return JSONResponse(
        status_code=exc.status_code,
        content=generic_resp.RespData[Union[dict, list, None]](
            error=True, message=exc.message, data=exc.data, error_detail=exc.detail
        ).model_dump(),
    )


async def defaultHttpExceptionHandler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=generic_resp.BaseResp(
            error=True,
            message="something went wrong",
            error_detail=str(exc),
        ).model_dump(),
    )

async def runTimeErrorHandler(request: Request, exc: RuntimeError):
    return JSONResponse(
        status_code=500,
        content=generic_resp.BaseResp(
            error=True,
            message="something went wrong",
            error_detail=str(exc),
        ).model_dump(),
    )

async def reqValidationErrExceptionHandler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content=generic_resp.BaseResp(
            error=True,
            message="request validation error",
            error_detail=exc.errors(),
        ).model_dump(),
    )


async def notFoundErrHandler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content=generic_resp.BaseResp(
            error=True,
            message="not found",
        ).model_dump(),
    )
