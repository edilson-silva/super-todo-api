from datetime import datetime
from typing import List

import pytest

from src.application.dtos.user.user_list_dto import UserListOutputDTO
from src.application.dtos.user.user_output_dto import UserOutputDTO
from src.application.usecases.user.user_list_usecase import UserListUseCase
from src.domain.entities.user_entity import User
from src.domain.entities.user_role import UserRole
from src.domain.repositories.user_repository import UserRepository


@pytest.fixture(autouse=True)
def setup(
    request,
    admin_company_users: List[User],
    user_repository: UserRepository,
):
    request.cls.users = admin_company_users
    request.cls.usecase = UserListUseCase(user_repository)


@pytest.mark.asyncio
class TestUserListUsecase:
    async def test_should_return_a_list_with_five_users(self):
        requester = self.users[0]
        usecase = self.usecase
        users_expected: List[User] = self.users

        response: UserListOutputDTO = await usecase.execute(requester, 10, 0)
        users: List[UserOutputDTO] = response.data

        assert isinstance(response, UserListOutputDTO)
        assert isinstance(users, list)
        assert len(users) == 6

        for user, user_expected in zip(users, users_expected):
            assert user.name == user_expected.name
            assert isinstance(user.id, str)
            assert user.id == user_expected.id
            assert user.name == user_expected.name
            assert user.email == user_expected.email
            assert isinstance(user.role, UserRole)
            assert user.role == user_expected.role
            assert isinstance(user.created_at, datetime)
            assert isinstance(user.updated_at, datetime)

    async def test_should_return_a_list_with_one_user(self):
        requester = self.users[0]
        usecase = self.usecase
        users_expected: List[User] = self.users[4:]

        response: UserListOutputDTO = await usecase.execute(requester, 10, 4)
        users: List[UserOutputDTO] = response.data

        assert isinstance(response, UserListOutputDTO)
        assert isinstance(users, list)
        assert len(users) == 2

        for user, user_expected in zip(users, users_expected):
            assert user.name == user_expected.name
            assert isinstance(user.id, str)
            assert user.id == user_expected.id
            assert user.name == user_expected.name
            assert user.email == user_expected.email
            assert isinstance(user.role, UserRole)
            assert user.role == user_expected.role
            assert isinstance(user.created_at, datetime)
            assert isinstance(user.updated_at, datetime)
