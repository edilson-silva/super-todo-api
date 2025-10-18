from datetime import datetime, timezone
from typing import List, Tuple

import pytest
from freezegun import freeze_time
from uuid_extensions import uuid7str

from src.application.dtos.user.user_update_dto import (
    UserUpdateInputDTO,
    UserUpdateOutputDTO,
)
from src.application.usecases.user.user_update_usecase import UserUpdateUseCase
from src.domain.entities.user_entity import User
from src.domain.entities.user_role import UserRole
from src.domain.exceptions.auth_exceptions import UnauthorizedException
from src.domain.exceptions.exceptions import NotFoundException
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher

SetupType = Tuple[List[User], UserUpdateUseCase]

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
class TestUserUpdateUsecase:
    @pytest.fixture
    def setup(
        self,
        admin_company_users: List[User],
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> SetupType:
        return admin_company_users, UserUpdateUseCase(
            user_repository, password_hasher
        )

    async def test_admin_user_can_update_any_user(self, setup: SetupType):
        users, usecase = setup
        requester = users[0]
        user_expected = users[1]
        user_expected_id = str(user_expected.id)

        user_update_dto = UserUpdateInputDTO(
            name='Updated Name',
            password='updated_pass',
            role=UserRole.USER,
            avatar='updated_avatar',
        )

        with freeze_time(mock_update_datetime):
            user_updated = await usecase.execute(
                requester, user_expected_id, user_update_dto
            )

        assert isinstance(user_updated, UserUpdateOutputDTO)
        assert user_updated.id == user_expected.id
        assert user_updated.name == user_update_dto.name
        assert user_updated.email == user_expected.email
        assert user_updated.avatar == user_update_dto.avatar
        assert user_updated.role == user_update_dto.role
        assert user_updated.created_at == user_expected.created_at
        assert isinstance(user_updated.created_at, datetime)
        assert user_updated.updated_at == mock_update_datetime

    async def test_non_admin_user_cannot_update_another_user(
        self, setup: SetupType
    ):
        users, usecase = setup
        requester = users[1]
        user_expected = users[0]
        user_expected_id = str(user_expected.id)

        user_update_dto = UserUpdateInputDTO(
            name='Updated Name',
            password='updated_pass',
            role=UserRole.USER,
            avatar='updated_avatar',
        )

        with pytest.raises(UnauthorizedException) as exc:
            await usecase.execute(requester, user_expected_id, user_update_dto)

        assert (
            str(exc.value)
            == "You don't have enough permission to perform this action"
        )

    async def test_invalid_id_should_raise_exception(self, setup: SetupType):
        users, usecase = setup
        requester = users[0]

        user_update_dto = UserUpdateInputDTO(
            name='Updated Name',
            password='updated_pass',
            role=UserRole.USER,
            avatar='updated_avatar',
        )

        with pytest.raises(NotFoundException) as exc:
            await usecase.execute(requester, uuid7str(), user_update_dto)

        assert str(exc.value) == 'Not found'
