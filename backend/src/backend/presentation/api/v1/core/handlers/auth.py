from fastapi.responses import JSONResponse
from jose import JWTError
from starlette import status

from src.backend.application.auth.errors import InvalidPasswordError
from fastapi import Request

async def invalid_password_exception_handler(
        request: Request,
        exc: InvalidPasswordError,
):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": str(exc),
            "status_code": status.HTTP_401_UNAUTHORIZED,
        }
    )
async def token_exception_handler(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Invalid Credentials",
            "status_code": status.HTTP_401_UNAUTHORIZED
        }
    )