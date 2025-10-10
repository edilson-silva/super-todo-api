from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.application.dtos.auth.auth_signin_dto import (
    AuthSigninInputDTO,
    AuthSigninOutputDTO,
)
from src.application.dtos.auth.auth_signup_dto import AuthSignupInputDTO
from src.application.usecases.auth.auth_signin_usecase import AuthSigninUseCase
from src.application.usecases.auth.auth_signup_usecase import AuthSignupUseCase
from src.core.container import AuthSigninUseCaseDep, AuthSignupUseCaseDep
from src.domain.exceptions.auth_exceptions import InvalidCredentialsException
from src.domain.exceptions.company_exceptions import (
    CompanyAlreadyRegisteredException,
)
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
    except CompanyAlreadyRegisteredException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Company already registered.',
        )


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
    try:
        input_dto = AuthSigninInputDTO(
            email=form_data.username,
            password=form_data.password,
        )
        return await use_case.execute(input_dto)
    except (NotFoundException, InvalidCredentialsException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
