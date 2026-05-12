import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    ValidationError,
)

logger = logging.getLogger(__name__)


DOMAIN_EXCEPTIONS = (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    ValidationError,
)


async def domain_exception_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    if not isinstance(exc, DOMAIN_EXCEPTIONS):
        raise exc

    error: dict[str, object] = {
        "code": exc.code,
        "message": exc.message,
    }

    if exc.details is not None:
        error["details"] = exc.details

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": error},
    )


async def unhandled_exception_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.error(
        "Unhandled exception while processing request",
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Erro interno do servidor.",
            },
        },
    )
