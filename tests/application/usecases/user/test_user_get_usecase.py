from datetime import datetime

import pytest
from uuid_extensions import uuid7str

from src.application.dtos.user.user_create_dto import UserCreateInputDTO
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_get_usecase import UserGetUseCase
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestUserGetUsecase:
    async def test_valid_id_should_return_found_user(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        user_create_dto = UserCreateInputDTO(
            name='Test User',
            email='test@example.com',
            password='123456789',
        )
        user_create_usecase = UserCreateUseCase(
            user_repository, password_hasher
        )

        user_created = await user_create_usecase.execute(user_create_dto)

        user_get_usecase = UserGetUseCase(user_repository)

        user_found = await user_get_usecase.execute(user_created.id)

        assert user_found.id == user_created.id
        assert user_found.name == user_created.name
        assert user_found.email == user_created.email
        assert user_found.role == user_created.role
        assert user_found.avatar == user_created.avatar
        assert isinstance(user_found.created_at, datetime)
        assert user_found.created_at == user_created.created_at
        assert isinstance(user_found.updated_at, datetime)
        assert user_found.updated_at == user_created.updated_at

    async def test_invalid_id_should_raise_exception(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        user_get_usecase = UserGetUseCase(user_repository)

        with pytest.raises(NotFoundException) as exc:
            await user_get_usecase.execute(uuid7str())

        assert str(exc.value) == 'Not found'
