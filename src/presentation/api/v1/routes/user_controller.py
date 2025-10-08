from fastapi import APIRouter, HTTPException, Query, status

from src.application.dtos.user.user_create_dto import (
    UserCreateInputDTO,
    UserCreateOutputDTO,
)
from src.application.dtos.user.user_get_dto import UserGetOutputDTO
from src.application.dtos.user.user_list_dto import UserListOutputDTO
from src.application.dtos.user.user_update_dto import (
    UserUpdateInputDTO,
    UserUpdateOutputDTO,
)
from src.application.dtos.user.user_update_partial_dto import (
    UserUpdatePartialInputDTO,
    UserUpdatePartialOutputDTO,
)
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_delete_usecase import UserDeleteUseCase
from src.application.usecases.user.user_get_usecase import UserGetUseCase
from src.application.usecases.user.user_list_usecase import UserListUseCase
from src.application.usecases.user.user_update_partial_usecase import (
    UserUpdatePartialUseCase,
)
from src.application.usecases.user.user_update_usecase import UserUpdateUseCase
from src.core.container import (
    GetLoggedUserUtilDep,
    UserCreateUseCaseDep,
    UserDeleteUseCaseDep,
    UserGetUseCaseDep,
    UserListUseCaseDep,
    UserUpdatePartialUseCaseDep,
    UserUpdateUseCaseDep,
)
from src.domain.exceptions.auth_exceptions import InvalidTokenException

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserCreateOutputDTO,
    status_code=status.HTTP_201_CREATED,
)
async def user_create(
    user: UserCreateInputDTO,
    use_case: UserCreateUseCase = UserCreateUseCaseDep,
    current_logged_user=GetLoggedUserUtilDep,
):
    """
    Create a new user.

    :param user: User creation data.
    :param use_case: UserCreateUseCase instance (injected dependency).

    Returns the created user.
    """
    try:
        created_user = await use_case.execute(
            current_logged_user.company_id, user
        )
        return created_user
    except InvalidTokenException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
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
        # Decode token and get company id
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
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0),
    use_case: UserListUseCase = UserListUseCaseDep,
):
    """
    Get the list of users.

    :param limit: Maximum number of users returned.
    :param offset: Number of users ignored in the search.
    :return: List of users.
    """
    # Decode token and get company id
    users = await use_case.execute(limit, offset)
    return users


@router.delete(
    '/{user_id}',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def user_delete(
    user_id: str,
    use_case: UserDeleteUseCase = UserDeleteUseCaseDep,
):
    """
    Delete a user based on its id.

    :param user_id: Id used to delete user.
    """
    try:
        # Decode token and get company id
        return await use_case.execute(user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put(
    '/{user_id}',
    response_model=UserUpdateOutputDTO,
    status_code=status.HTTP_200_OK,
)
async def user_update(
    user_id: str,
    data: UserUpdateInputDTO,
    use_case: UserUpdateUseCase = UserUpdateUseCaseDep,
):
    """
    Update a user based on its id.

    :param user_id: Id used to delete user.
    :param data: User update data.
    :param use_case: UserUpdateUseCase instance (injected dependency).

    Returns the updated user.
    """
    try:
        # Decode token and get company id
        updated_user = await use_case.execute(user_id, data)
        return updated_user
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch(
    '/{user_id}',
    response_model=UserUpdatePartialOutputDTO,
    status_code=status.HTTP_200_OK,
)
async def user_update_partial(
    user_id: str,
    data: UserUpdatePartialInputDTO,
    use_case: UserUpdatePartialUseCase = UserUpdatePartialUseCaseDep,
):
    """
    Update a user based on its id.

    :param user_id: Id used to delete user.
    :param data: User update data.
    :param use_case: UserUpdatePartialUseCase instance (injected dependency).

    Returns the updated user.
    """
    try:
        # Decode token and get company id
        updated_user = await use_case.execute(user_id, data)
        return updated_user
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
