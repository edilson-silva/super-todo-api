from datetime import datetime
from typing import List, Tuple

import pytest
from uuid_extensions import uuid7str

from src.application.usecases.user.user_get_usecase import UserGetUseCase
from src.domain.entities.user_entity import User
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository

SetupType = Tuple[List[User], UserGetUseCase]


@pytest.mark.asyncio
class TestUserGetUsecase:
    @pytest.fixture
    def setup(
        self,
        admin_company_users: List[User],
        user_repository: UserRepository,
    ):
        return admin_company_users, UserGetUseCase(user_repository)

    async def test_valid_id_should_return_found_user(self, setup: SetupType):
        users, usecase = setup
        requester = users[0]
        user_expected = users[1]
        user_expected_id = str(user_expected.id)

        user_found = await usecase.execute(requester, user_expected_id)

        assert user_found.id == user_expected.id
        assert user_found.name == user_expected.name
        assert user_found.email == user_expected.email
        assert user_found.role == user_expected.role
        assert user_found.avatar == user_expected.avatar
        assert isinstance(user_found.created_at, datetime)
        assert user_found.created_at == user_expected.created_at
        assert isinstance(user_found.updated_at, datetime)
        assert user_found.updated_at == user_expected.updated_at

    async def test_invalid_id_should_raise_exception(self, setup: SetupType):
        users, usecase = setup
        requester = users[0]

        with pytest.raises(NotFoundException) as exc:
            await usecase.execute(requester, uuid7str())

        assert str(exc.value) == 'Not found'
