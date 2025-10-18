from datetime import datetime, timezone
from typing import List, Tuple

import pytest
from freezegun import freeze_time
from uuid_extensions import uuid7str

from src.application.dtos.user.user_update_partial_dto import (
    UserUpdatePartialInputDTO,
    UserUpdatePartialOutputDTO,
)
from src.application.usecases.user.user_update_partial_usecase import (
    UserUpdatePartialUseCase,
)
from src.domain.entities.user_entity import User
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.auth_exceptions import UnauthorizedException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher

SetupType = Tuple[List[User], UserUpdatePartialUseCase]

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
    @pytest.fixture
    def setup(
        self,
        admin_company_users: List[User],
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> SetupType:
        return admin_company_users, UserUpdatePartialUseCase(
            user_repository, password_hasher
        )

    async def test_valid_id_with_empty_properties_should_return_user_info(
        self, setup: SetupType
    ):
        users, usecase = setup
        requester = users[0]
        user_expected = users[1]
        user_expected_id = str(user_expected.id)

        user_update_partial_dto = UserUpdatePartialInputDTO()

        user_updated = await usecase.execute(
            requester, user_expected_id, user_update_partial_dto
        )

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_expected.id
        assert user_updated.name == user_updated.name
        assert user_updated.email == user_expected.email
        assert user_updated.avatar == user_expected.avatar
        assert user_updated.role == user_expected.role
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.created_at == user_expected.created_at
        assert isinstance(user_updated.updated_at, datetime)
        assert user_updated.updated_at == user_expected.updated_at

    async def test_valid_id_with_new_name_should_return_updated_user_info(
        self, setup: SetupType
    ):
        users, usecase = setup
        requester = users[0]
        user_expected = users[1]
        user_expected_id = str(user_expected.id)

        user_update_partial_dto = UserUpdatePartialInputDTO(
            name='Updated Name',
        )

        with freeze_time(mock_update_datetime):
            user_updated = await usecase.execute(
                requester, user_expected_id, user_update_partial_dto
            )

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_expected.id
        assert user_updated.name == user_update_partial_dto.name
        assert user_updated.email == user_expected.email
        assert user_updated.avatar == user_expected.avatar
        assert user_updated.role == user_expected.role
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.created_at == user_expected.created_at
        assert isinstance(user_updated.updated_at, datetime)
        assert user_updated.updated_at == mock_update_datetime

    async def test_valid_id_with_new_password_should_return_updated_user_info(
        self,
        setup: SetupType,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        users, usecase = setup
        requester = users[0]
        user_expected = users[1]
        user_expected_id = str(user_expected.id)

        user_update_password = 'updated_pass'
        user_update_password_hashed = await password_hasher.async_hash(
            user_update_password
        )

        user_update_partial_dto = UserUpdatePartialInputDTO(
            password='updated_pass',
        )

        with freeze_time(mock_update_datetime):
            user_updated = await usecase.execute(
                requester, user_expected_id, user_update_partial_dto
            )

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_expected.id
        assert user_updated.name == user_expected.name
        assert user_updated.email == user_expected.email
        assert user_updated.avatar == user_expected.avatar
        assert user_updated.role == user_expected.role
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.created_at == user_expected.created_at
        assert isinstance(user_updated.updated_at, datetime)
        assert user_updated.updated_at == mock_update_datetime

        found_user = await user_repository.find_by_id(
            user_expected_id,
            str(requester.company_id),
        )

        assert found_user is not None
        assert found_user.password != user_update_password_hashed

    async def test_valid_id_with_new_role_should_return_updated_user_info(
        self, setup: SetupType
    ):
        users, usecase = setup
        requester = users[0]
        user_expected = users[1]
        user_expected_id = str(user_expected.id)

        user_update_partial_dto = UserUpdatePartialInputDTO(
            role=UserRole.USER,
        )

        with freeze_time(mock_update_datetime):
            user_updated = await usecase.execute(
                requester, user_expected_id, user_update_partial_dto
            )

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_expected.id
        assert user_updated.name == user_expected.name
        assert user_updated.email == user_expected.email
        assert user_updated.avatar == user_expected.avatar
        assert user_updated.role == user_update_partial_dto.role
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.created_at == user_expected.created_at
        assert isinstance(user_updated.updated_at, datetime)
        assert user_updated.updated_at == mock_update_datetime

    async def test_valid_id_with_new_avatar_should_return_updated_user_info(
        self, setup: SetupType
    ):
        users, usecase = setup
        requester = users[0]
        user_expected = users[1]
        user_expected_id = str(user_expected.id)

        user_update_partial_dto = UserUpdatePartialInputDTO(
            avatar='updated_avatar',
        )

        with freeze_time(mock_update_datetime):
            user_updated = await usecase.execute(
                requester, user_expected_id, user_update_partial_dto
            )

        assert isinstance(user_updated, UserUpdatePartialOutputDTO)
        assert user_updated.id == user_expected.id
        assert user_updated.name == user_expected.name
        assert user_updated.email == user_expected.email
        assert user_updated.avatar == user_update_partial_dto.avatar
        assert user_updated.role == user_expected.role
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.created_at == user_expected.created_at
        assert isinstance(user_updated.updated_at, datetime)
        assert user_updated.updated_at == mock_update_datetime

    async def test_non_admin_user_cannot_update_another_user(
        self, setup: SetupType
    ):
        users, usecase = setup
        requester = users[1]
        user_expected = users[0]
        user_expected_id = str(user_expected.id)

        user_update_partial_dto = UserUpdatePartialInputDTO(
            name='Updated Name',
            password='updated_pass',
            role=UserRole.USER,
            avatar='updated_avatar',
        )

        with pytest.raises(UnauthorizedException) as exc:
            await usecase.execute(
                requester, user_expected_id, user_update_partial_dto
            )

        assert (
            str(exc.value)
            == "You don't have enough permission to perform this action"
        )

    async def test_invalid_id_should_raise_exception(self, setup: SetupType):
        users, usecase = setup
        requester = users[0]

        user_update_partial_dto = UserUpdatePartialInputDTO(
            name='Updated Name',
            password='updated_pass',
            role=UserRole.USER,
            avatar='updated_avatar',
        )

        with pytest.raises(NotFoundException) as exc:
            await usecase.execute(
                requester, uuid7str(), user_update_partial_dto
            )

        assert str(exc.value) == 'Not found'
