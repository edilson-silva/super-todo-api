from fastapi import FastAPI, Request, status
from starlette.responses import JSONResponse

from src.domain.exceptions.auth_exceptions import (
    InvalidTokenException,
    UnauthorizedException,
)
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.exceptions.user_exceptions import UserAlreadyExistsException


def http_exception_handler(app: FastAPI):
    @app.exception_handler(UserAlreadyExistsException)
    async def general_exception_handler(
        request: Request, exc: UserAlreadyExistsException
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'details': str(exc)},
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_exception_handler(
        request: Request, exc: InvalidTokenException
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={'details': str(exc)},
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_exception_handler(
        request: Request, exc: UnauthorizedException
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={'details': str(exc)},
        )

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(
        request: Request, exc: NotFoundException
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'details': str(exc)},
        )
