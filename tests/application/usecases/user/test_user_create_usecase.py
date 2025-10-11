from datetime import datetime, timezone

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


@pytest.mark.asyncio
class TestUserCreateUsecase:
    company_id = uuid7str()

    @freeze_time(mock_datetime)
    async def test_new_user_info_should_return_created_user(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        admin_user: User,
        basic_user_info: dict,
    ):
        user_create_dto = UserCreateInputDTO(
            name=basic_user_info['name'],
            email=basic_user_info['email'],
            password=basic_user_info['password'],
        )
        user_create_usecase = UserCreateUseCase(
            user_repository,
            password_hasher,
        )

        user = await user_create_usecase.execute(admin_user, user_create_dto)

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
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        admin_user: User,
        admin_user_info: dict,
    ):
        user_create_dto = UserCreateInputDTO(
            name=admin_user_info['name'],
            email=admin_user_info['email'],
            password=admin_user_info['password'],
        )
        user_create_usecase = UserCreateUseCase(
            user_repository, password_hasher
        )

        with pytest.raises(UserAlreadyExistsException) as exc:
            await user_create_usecase.execute(admin_user, user_create_dto)

        assert str(exc.value) == 'Email already registered'
