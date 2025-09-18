from fastapi import APIRouter, HTTPException, status

from src.application.dtos.user.user_create_dto import (
    UserCreateInputDTO,
    UserCreateOutputDTO,
)
from src.application.dtos.user.user_get_dto import UserGetOutputDTO
from src.application.dtos.user.user_list_dto import UserListOutputDTO
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_get_usecase import UserGetUseCase
from src.application.usecases.user.user_list_usecase import UserListUseCase
from src.core.container import (
    UserCreateUseCaseDep,
    UserGetUseCaseDep,
    UserListUseCaseDep,
)

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
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get(
    '/{user_id}',
    response_model=UserGetOutputDTO,
    status_code=status.HTTP_200_OK,
)
async def user_get(
    user_id: str,
    use_case: UserGetUseCase = UserGetUseCaseDep,
):
    """
    Get a user based on its id.

    :param user_id: Id used to get user.

    :return: Found user info.
    """
    try:
        user = await use_case.execute(user_id)
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    '/',
    response_model=UserListOutputDTO,
    status_code=status.HTTP_200_OK,
)
async def user_list(
    use_case: UserListUseCase = UserListUseCaseDep,
):
    """
    Get the list of users.

    :return: List of users.
    """
    users = await use_case.execute()
    return users
