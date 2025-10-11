from typing import List

import pytest
from uuid_extensions import uuid7str

from src.application.usecases.user.user_delete_usecase import UserDeleteUseCase
from src.domain.entities.user_entity import User
from src.domain.exceptions.auth_exceptions import UnauthorizedException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository


@pytest.fixture(autouse=True)
def setup(
    request, admin_company_users: List[User], user_repository: UserRepository
):
    request.cls.users = admin_company_users
    request.cls.usecase = UserDeleteUseCase(user_repository)


@pytest.mark.asyncio
class TestUserDeleteUsecase:
    async def test_found_user_should_be_deleted_and_return_success(self):
        requester = self.users[0]
        user_id = str(self.users[1].id)

        user_deleted = await self.usecase.execute(requester, user_id)

        assert user_deleted is None

    async def test_not_found_user_should_raise_exception(self):
        requester = self.users[0]

        with pytest.raises(NotFoundException) as exc:
            await self.usecase.execute(requester, uuid7str())

        assert str(exc.value) == 'Not found'

    async def test_non_admin_requester_should_raise_exception(self):
        requester = self.users[1]
        user_id = str(self.users[2].id)

        with pytest.raises(UnauthorizedException) as exc:
            await self.usecase.execute(requester, user_id)

        assert str(exc.value) == 'Unauthorized'

    async def test_self_delete_should_raise_exception(self):
        requester = self.users[0]
        user_id = str(self.users[0].id)

        with pytest.raises(UnauthorizedException) as exc:
            await self.usecase.execute(requester, user_id)

        assert (
            str(exc.value) == 'You are not allowed to delete your own account.'
        )
