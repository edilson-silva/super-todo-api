from fastapi import APIRouter, HTTPException, status

from src.application.dtos.auth.auth_login_dto import (
    AuthLoginInputDTO,
    AuthLoginOutputDTO,
)
from src.application.dtos.auth.auth_signup_dto import AuthSignupInputDTO
from src.application.usecases.auth.auth_login_usecase import AuthLoginUseCase
from src.application.usecases.auth.auth_singup_usecase import AuthSignupUseCase
from src.core.container import AuthLoginUseCaseDep, AuthSignupUseCaseDep
from src.domain.exceptions.auth_exceptions import InvalidCredentialsException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.exceptions.user_exceptions import UserAlreadyExistsException

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    input_dto: AuthSignupInputDTO,
    use_case: AuthSignupUseCase = AuthSignupUseCaseDep,
):
    """
    Perform signup for a new user based on its unique **email**.
    """
    try:
        return await use_case.execute(input_dto)
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
        )


@router.post(
    '/login',
    status_code=status.HTTP_201_CREATED,
)
async def login(
    input_dto: AuthLoginInputDTO,
    use_case: AuthLoginUseCase = AuthLoginUseCaseDep,
) -> AuthLoginOutputDTO:
    """
    Perform login for a user based on email and password.

    :return: User info
    """
    try:
        return await use_case.execute(input_dto)
    except (NotFoundException, InvalidCredentialsException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
