from typing import List, Tuple

import pytest
from uuid_extensions import uuid7str

from src.application.usecases.user.user_delete_usecase import UserDeleteUseCase
from src.domain.entities.user_entity import User
from src.domain.exceptions.auth_exceptions import UnauthorizedException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository

SetupType = Tuple[List[User], UserDeleteUseCase]


@pytest.mark.asyncio
class TestUserDeleteUsecase:
    @pytest.fixture
    def setup(
        self, admin_company_users: List[User], user_repository: UserRepository
    ):
        return admin_company_users, UserDeleteUseCase(user_repository)

    async def test_found_user_should_be_deleted_and_return_success(
        self, setup: SetupType
    ):
        users, usecase = setup
        requester = users[0]
        user_id = str(users[1].id)

        user_deleted = await usecase.execute(requester, user_id)

        assert user_deleted is None

    async def test_not_found_user_should_raise_exception(
        self, setup: SetupType
    ):
        users, usecase = setup
        requester = users[0]

        with pytest.raises(NotFoundException) as exc:
            await usecase.execute(requester, uuid7str())

        assert str(exc.value) == 'Not found'

    async def test_non_admin_requester_should_raise_exception(
        self, setup: SetupType
    ):
        users, usecase = setup
        requester = users[1]
        user_id = str(users[2].id)

        with pytest.raises(UnauthorizedException) as exc:
            await usecase.execute(requester, user_id)

        assert str(exc.value) == 'Unauthorized'

    async def test_self_delete_should_raise_exception(self, setup: SetupType):
        users, usecase = setup
        requester = users[0]
        user_id = str(users[0].id)

        with pytest.raises(UnauthorizedException) as exc:
            await usecase.execute(requester, user_id)

        assert (
            str(exc.value) == 'You are not allowed to delete your own account'
        )
