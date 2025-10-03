from datetime import datetime, timezone

import pytest
from freezegun import freeze_time
from uuid_extensions import uuid7str

from src.application.dtos.user.user_create_dto import UserCreateInputDTO
from src.application.dtos.user.user_update_partial_dto import (
    UserUpdatePartialInputDTO,
    UserUpdatePartialOutputDTO,
)
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_update_partial_usecase import (
    UserUpdatePartialUseCase,
)
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher

mock_create_datetime = datetime(
    2025,
    1,
    1,
    0,
    0,
    0,
    0,
    timezone.utc,
)
mock_update_datetime = datetime(
    2025,
    1,
    1,
    0,
    5,
    0,
    0,
    timezone.utc,
)


@pytest.mark.asyncio
class TestUserUpdatePartialUsecase:
    company_id = uuid7str()
    user_create_dto = UserCreateInputDTO(
        name='Test User',
        email='test@example.com',
        password='123456789',
        company_id=company_id,
    )

    async def test_valid_id_with_empty_properties_should_return_user_info(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        user_create_usecase = UserCreateUseCase(
            user_repository, password_hasher
        )

        with freeze_time(mock_create_datetime):
            user_created = await user_create_usecase.execute(
                self.user_create_dto
            )

        user_update_partial_dto = UserUpdatePartialInputDTO()
        user_update_partial_usecase = UserUpdatePartialUseCase(
            user_repository, password_hasher
        )

        with freeze_time(mock_update_datetime):
            user_updated = await user_update_partial_usecase.execute(
                user_created.id, self.company_id, user_update_partial_dto
            )

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_created.id
        assert user_updated.name == user_updated.name
        assert user_updated.email == user_created.email
        assert user_updated.avatar == user_created.avatar
        assert user_updated.role == user_created.role
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.created_at == mock_create_datetime
        assert isinstance(user_updated.updated_at, datetime)
        assert user_updated.updated_at == mock_create_datetime

    async def test_valid_id_with_new_name_should_return_updated_user_info(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        user_create_usecase = UserCreateUseCase(
            user_repository, password_hasher
        )

        with freeze_time(mock_create_datetime):
            user_created = await user_create_usecase.execute(
                self.user_create_dto
            )

        user_update_partial_dto = UserUpdatePartialInputDTO(
            name='Updated Name',
        )
        user_update_partial_usecase = UserUpdatePartialUseCase(
            user_repository, password_hasher
        )

        with freeze_time(mock_update_datetime):
            user_updated = await user_update_partial_usecase.execute(
                user_created.id, self.company_id, user_update_partial_dto
            )

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_created.id
        assert user_updated.name == user_update_partial_dto.name
        assert user_updated.email == user_created.email
        assert user_updated.avatar == user_created.avatar
        assert user_updated.role == user_created.role
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.created_at == mock_create_datetime
        assert isinstance(user_updated.updated_at, datetime)
        assert user_updated.updated_at == mock_update_datetime

    async def test_valid_id_with_new_password_should_return_updated_user_info(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        user_create_usecase = UserCreateUseCase(
            user_repository, password_hasher
        )

        with freeze_time(mock_create_datetime):
            user_created = await user_create_usecase.execute(
                self.user_create_dto
            )

        user_update_partial_dto = UserUpdatePartialInputDTO(
            password='updated_pass',
        )
        user_update_partial_usecase = UserUpdatePartialUseCase(
            user_repository, password_hasher
        )

        with freeze_time(mock_update_datetime):
            user_updated = await user_update_partial_usecase.execute(
                user_created.id, self.company_id, user_update_partial_dto
            )

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_created.id
        assert user_updated.name == user_created.name
        assert user_updated.email == user_created.email
        assert user_updated.avatar == user_created.avatar
        assert user_updated.role == user_created.role
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.created_at == mock_create_datetime
        assert isinstance(user_updated.updated_at, datetime)
        assert user_updated.updated_at == mock_update_datetime

        found_user = await user_repository.find_by_id(
            user_created.id,
            self.company_id,
        )

        assert found_user is not None
        assert found_user.password != ''

    async def test_valid_id_with_new_role_should_return_updated_user_info(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        user_create_usecase = UserCreateUseCase(
            user_repository, password_hasher
        )

        with freeze_time(mock_create_datetime):
            user_created = await user_create_usecase.execute(
                self.user_create_dto
            )

        user_update_partial_dto = UserUpdatePartialInputDTO(
            role=UserRole.USER,
        )
        user_update_partial_usecase = UserUpdatePartialUseCase(
            user_repository, password_hasher
        )

        with freeze_time(mock_update_datetime):
            user_updated = await user_update_partial_usecase.execute(
                user_created.id, self.company_id, user_update_partial_dto
            )

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_created.id
        assert user_updated.name == user_created.name
        assert user_updated.email == user_created.email
        assert user_updated.avatar == user_created.avatar
        assert user_updated.role == user_update_partial_dto.role
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.created_at == mock_create_datetime
        assert isinstance(user_updated.updated_at, datetime)
        assert user_updated.updated_at == mock_update_datetime

    async def test_valid_id_with_new_avatar_should_return_updated_user_info(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        user_create_usecase = UserCreateUseCase(
            user_repository, password_hasher
        )

        with freeze_time(mock_create_datetime):
            user_created = await user_create_usecase.execute(
                self.user_create_dto
            )

        user_update_partial_dto = UserUpdatePartialInputDTO(
            avatar='updated_avatar',
        )
        user_update_partial_usecase = UserUpdatePartialUseCase(
            user_repository, password_hasher
        )

        with freeze_time(mock_update_datetime):
            user_updated = await user_update_partial_usecase.execute(
                user_created.id, self.company_id, user_update_partial_dto
            )

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_created.id
        assert user_updated.name == user_created.name
        assert user_updated.email == user_created.email
        assert user_updated.avatar == user_update_partial_dto.avatar
        assert user_updated.role == user_created.role
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.created_at == mock_create_datetime
        assert isinstance(user_updated.updated_at, datetime)
        assert user_updated.updated_at == mock_update_datetime

    async def test_invalid_id_should_raise_exception(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        user_update_partial_dto = UserUpdatePartialInputDTO(
            name='Updated Name',
            password='updated_pass',
            role=UserRole.USER,
            avatar='updated_avatar',
        )
        user_update_partial_usecase = UserUpdatePartialUseCase(
            user_repository, password_hasher
        )

        with pytest.raises(NotFoundException) as exc:
            await user_update_partial_usecase.execute(
                uuid7str(), self.company_id, user_update_partial_dto
            )

        assert str(exc.value) == 'Not found'
