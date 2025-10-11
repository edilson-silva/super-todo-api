from datetime import datetime, timezone
from typing import List

import pytest
from freezegun import freeze_time
from uuid_extensions import uuid7str

from src.application.dtos.user.user_create_dto import (
    UserCreateInputDTO,
    UserCreateOutputDTO,
)
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.domain.entities.user_entity import User
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.auth_exceptions import UnauthorizedException
from src.domain.exceptions.user_exceptions import UserAlreadyExistsException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher

mock_datetime = datetime(
    2025,
    1,
    1,
    0,
    0,
    0,
    0,
    timezone.utc,
)


@pytest.fixture(autouse=True)
def setup(
    request,
    admin_company_users: List[User],
    user_repository: UserRepository,
    password_hasher: PasswordHasher,
):
    request.cls.users = admin_company_users
    request.cls.usecase = UserCreateUseCase(
        user_repository,
        password_hasher,
    )


@pytest.mark.asyncio
class TestUserCreateUsecase:
    company_id = uuid7str()

    @freeze_time(mock_datetime)
    async def test_new_user_info_should_return_created_user(
        self, basic_user_info: dict
    ):
        requester = self.users[0]
        usecase = self.usecase

        user_create_dto = UserCreateInputDTO(
            name=basic_user_info['name'],
            email=basic_user_info['email'],
            password=basic_user_info['password'],
        )

        user = await usecase.execute(requester, user_create_dto)

        assert isinstance(user, UserCreateOutputDTO)

        assert user is not None
        assert isinstance(user.id, str)
        assert user.id != ''
        assert user.name == user_create_dto.name
        assert user.email == user_create_dto.email
        assert user.role == UserRole.ADMIN
        assert isinstance(user.created_at, datetime)
        assert user.created_at == mock_datetime
        assert isinstance(user.updated_at, datetime)
        assert user.updated_at == mock_datetime

    async def test_existing_user_should_raise_exception(
        self, admin_user_info: dict
    ):
        requester = self.users[0]
        usecase = self.usecase

        user_create_dto = UserCreateInputDTO(
            name=admin_user_info['name'],
            email=admin_user_info['email'],
            password=admin_user_info['password'],
        )

        with pytest.raises(UserAlreadyExistsException) as exc:
            await usecase.execute(requester, user_create_dto)

        assert str(exc.value) == 'Email already registered'

    async def test_non_admin_requester_should_raise_exception(
        self, basic_user_info: dict
    ):
        requester = self.users[1]
        usecase = self.usecase

        user_create_dto = UserCreateInputDTO(
            name=basic_user_info['name'],
            email=basic_user_info['email'],
            password=basic_user_info['password'],
        )

        with pytest.raises(UnauthorizedException) as exc:
            await usecase.execute(requester, user_create_dto)

        assert str(exc.value) == 'Unauthorized'
