from datetime import datetime

import pytest

from src.application.dtos.user.user_create_dto import UserCreateInputDTO
from src.application.dtos.user.user_list_dto import UserListOutputDTO
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_list_usecase import UserListUseCase
from src.domain.entities.user_role import UserRole
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestUserListUsecase:
    async def test_should_return_an_empty_users_list(
        self,
        user_repository: UserRepository,
    ):
        user_list_usecase = UserListUseCase(user_repository)

        users = await user_list_usecase.execute(10, 0)

        assert isinstance(users, UserListOutputDTO)
        assert users.data == []

    async def test_should_return_a_list_with_two_users(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        user_create_dto_1 = UserCreateInputDTO(
            name='User1',
            email='test1@example.com',
            password='123456789',
        )
        user_create_dto_2 = UserCreateInputDTO(
            name='User2',
            email='test2@example.com',
            password='123456789',
        )

        user_create_usecase = UserCreateUseCase(
            user_repository, password_hasher
        )

        await user_create_usecase.execute(user_create_dto_1)
        await user_create_usecase.execute(user_create_dto_2)
        user_list_usecase = UserListUseCase(user_repository)

        users = await user_list_usecase.execute(10, 0)

        assert isinstance(users, UserListOutputDTO)
        assert len(users.data) == 2

        user_list_user_1 = users.data[0]

        assert user_list_user_1.name == user_create_dto_1.name
        assert isinstance(user_list_user_1.id, str)
        assert user_list_user_1.id != ''
        assert user_list_user_1.name == user_create_dto_1.name
        assert user_list_user_1.email == user_create_dto_1.email
        assert user_list_user_1.role == UserRole.ADMIN
        assert isinstance(user_list_user_1.created_at, datetime)

        user_list_user_2 = users.data[1]

        assert user_list_user_2.name == user_create_dto_2.name
        assert isinstance(user_list_user_2.id, str)
        assert user_list_user_2.id != ''
        assert user_list_user_2.name == user_create_dto_2.name
        assert user_list_user_2.email == user_create_dto_2.email
        assert user_list_user_2.role == UserRole.ADMIN
        assert isinstance(user_list_user_2.created_at, datetime)

    async def test_should_return_a_list_with_one_user(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        user_create_dto_1 = UserCreateInputDTO(
            name='User1',
            email='test1@example.com',
            password='123456789',
        )
        user_create_dto_2 = UserCreateInputDTO(
            name='User2',
            email='test2@example.com',
            password='123456789',
        )

        user_create_usecase = UserCreateUseCase(
            user_repository, password_hasher
        )

        await user_create_usecase.execute(user_create_dto_1)
        await user_create_usecase.execute(user_create_dto_2)
        user_list_usecase = UserListUseCase(user_repository)

        users = await user_list_usecase.execute(10, 1)

        assert isinstance(users, UserListOutputDTO)
        assert len(users.data) == 1

        user_list_user_2 = users.data[0]

        assert user_list_user_2.name == user_create_dto_2.name
        assert isinstance(user_list_user_2.id, str)
        assert user_list_user_2.id != ''
        assert user_list_user_2.name == user_create_dto_2.name
        assert user_list_user_2.email == user_create_dto_2.email
        assert user_list_user_2.role == UserRole.ADMIN
        assert isinstance(user_list_user_2.created_at, datetime)
