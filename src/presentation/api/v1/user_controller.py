from fastapi import APIRouter, HTTPException, status

from src.application.dtos.user.user_create_dto import (
    UserCreateInputDTO,
    UserCreateOutputDTO,
)
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.core.container import UserCreateUseCaseDep

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserCreateOutputDTO,
    status_code=status.HTTP_201_CREATED,
)
async def user_create(
    user: UserCreateInputDTO,
    use_case: UserCreateUseCase = UserCreateUseCaseDep,
):
    """
    Create a new user.

    :param user: User creation data.
    :param use_case: UserCreateUseCase instance (injected dependency).

    Returns the created user.
    """
    try:
        created_user = await use_case.execute(user)
        return created_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
