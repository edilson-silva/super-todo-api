from datetime import datetime, timezone
from uuid import UUID

import pytest
from freezegun import freeze_time

from src.domain.entities.user_entity import User, UserRole
from src.domain.repositories.user_repository import UserRepository

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
class TestUserRepository:
    @freeze_time(mock_datetime)
    async def test_should_create_an_user(
        self, user_repository: UserRepository
    ):
        user = User(
            name='User 1',
            email='user1@test.com',
            password='123456789',
            role=UserRole.ADMIN,
        )

        created_user = await user_repository.create(user)

        assert isinstance(created_user.id, UUID)
        assert created_user.name == user.name
        assert created_user.email == user.email
        assert created_user.password == user.password
        assert created_user.role == user.role
        assert created_user.avatar == user.avatar
        assert isinstance(created_user.created_at, datetime)
        assert created_user.created_at == mock_datetime

        found_user = await user_repository.find_by_id(str(created_user.id))

        assert found_user
