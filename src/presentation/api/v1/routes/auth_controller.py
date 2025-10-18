from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.application.dtos.auth.auth_signin_dto import (
    AuthSigninInputDTO,
    AuthSigninOutputDTO,
)
from src.application.dtos.auth.auth_signup_dto import AuthSignupInputDTO
from src.application.usecases.auth.auth_signin_usecase import AuthSigninUseCase
from src.application.usecases.auth.auth_signup_usecase import AuthSignupUseCase
from src.core.container import AuthSigninUseCaseDep, AuthSignupUseCaseDep

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
    return await use_case.execute(input_dto)


@router.post(
    '/signin',
    status_code=status.HTTP_200_OK,
)
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: AuthSigninUseCase = AuthSigninUseCaseDep,
) -> AuthSigninOutputDTO:
    """
    Perform signin for a user based on email and password.

    :param form_data: OAuth2 form data with username and password.

    :return: Access token.
    """
    input_dto = AuthSigninInputDTO(
        email=form_data.username,
        password=form_data.password,
    )
    return await use_case.execute(input_dto)
