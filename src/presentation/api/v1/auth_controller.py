from fastapi import APIRouter, HTTPException, status

from src.application.dtos.auth.auth_signup_dto import AuthSignupInputDTO
from src.application.usecases.auth.auth_singup_usecase import AuthSignupUseCase
from src.core.container import AuthSignupUseCaseDep
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
