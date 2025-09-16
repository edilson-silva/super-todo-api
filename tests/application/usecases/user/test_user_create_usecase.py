from datetime import datetime

import pytest

from src.application.dtos.user.user_create_dto import (
    UserCreateInputDTO,
    UserCreateOutputDTO,
)
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.domain.entities.user_role import UserRole
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestUserCreateUsecase:
    async def test_new_user_info_should_return_created_user(
        self,
        fake_user_repository: UserRepository,
        fake_password_hasher: PasswordHasher,
    ):
        user_create_dto = UserCreateInputDTO(
            name='Test User',
            email='test@example.com',
            password='123456789',
        )
        user_create_usecase = UserCreateUseCase(
            fake_user_repository, fake_password_hasher
        )

        user = await user_create_usecase.execute(user_create_dto)

        assert isinstance(user, UserCreateOutputDTO)

        assert user is not None
        assert isinstance(user.id, str)
        assert user.id != ''
        assert user.name == user_create_dto.name
        assert user.email == user_create_dto.email
        assert user.password == f'hashed_{user_create_dto.password}'
        assert user.role == UserRole.ADMIN
        assert isinstance(user.created_at, datetime)
