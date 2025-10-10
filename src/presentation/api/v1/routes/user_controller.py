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
    GetRequesterFromTokenDep,
    UserCreateUseCaseDep,
    UserDeleteUseCaseDep,
    UserGetUseCaseDep,
    UserListUseCaseDep,
    UserUpdatePartialUseCaseDep,
    UserUpdateUseCaseDep,
)
from src.domain.entities.user_entity import User

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserCreateOutputDTO,
    status_code=status.HTTP_201_CREATED,
)
async def user_create(
    user: UserCreateInputDTO,
    requester: User = GetRequesterFromTokenDep,
    use_case: UserCreateUseCase = UserCreateUseCaseDep,
):
    """
    To create a user, the requester must be admin.\n
    Returns the created user.
    """
    return await use_case.execute(requester, user)


@router.get(
    '/{user_id}',
    response_model=UserGetOutputDTO,
    status_code=status.HTTP_200_OK,
)
async def user_get(
    user_id: str,
    requester: User = GetRequesterFromTokenDep,
    use_case: UserGetUseCase = UserGetUseCaseDep,
):
    """
    To get a user, the requester must be from the same company.\n
    Return user info.
    """
    return await use_case.execute(requester, user_id)


@router.get(
    '/',
    response_model=UserListOutputDTO,
    status_code=status.HTTP_200_OK,
)
async def user_list(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0),
    requester: User = GetRequesterFromTokenDep,
    use_case: UserListUseCase = UserListUseCaseDep,
):
    """
    To list users, the requester must be admin.\n
    Returns the list of found users.
    """
    return await use_case.execute(requester, limit, offset)


@router.delete(
    '/{user_id}',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def user_delete(
    user_id: str,
    requester: User = GetRequesterFromTokenDep,
    use_case: UserDeleteUseCase = UserDeleteUseCaseDep,
):
    """
    To delete a user, the requester must be admin.\n
    Returns nothing.
    """
    return await use_case.execute(requester, user_id)


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
