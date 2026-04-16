from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from src.backend.application.shared.errors import ConflictError


async def conflict_error_handler(request: Request, exc: ConflictError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
            "status_code": status.HTTP_409_CONFLICT,
        }
    )