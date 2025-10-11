from typing import List

import pytest
from uuid_extensions import uuid7str

from src.application.usecases.user.user_delete_usecase import UserDeleteUseCase
from src.domain.entities.user_entity import User
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestUserDeleteUsecase:
    async def test_found_user_should_be_deleted_and_return_success(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        admin_company_users: List[User],
        admin_user_info: dict,
    ):
        requester = admin_company_users[0]
        user_id = str(admin_company_users[1].id)

        user_delete_usecase = UserDeleteUseCase(user_repository)

        user_deleted = await user_delete_usecase.execute(
            requester,
            user_id,
        )

        assert user_deleted is None

    async def test_not_found_user_should_raise_exception(
        self,
        user_repository: UserRepository,
        admin_user: User,
    ):
        user_delete_usecase = UserDeleteUseCase(user_repository)

        with pytest.raises(NotFoundException) as exc:
            await user_delete_usecase.execute(
                admin_user,
                uuid7str(),
            )

        assert str(exc.value) == 'Not found'
