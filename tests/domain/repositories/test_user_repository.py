from datetime import datetime, timezone

import pytest

from src.domain.entities.user_entity import User
from src.domain.repositories.user_repository import UserRepository


@pytest.mark.asyncio
class TestUserRepository:
    async def test_should_create_two_users(
        self, fake_user_repository: UserRepository
    ):
        user_1 = User(
            name='User 1',
            email='user1@test.com',
            password='123456789',
        )

        created_user_1 = await fake_user_repository.create(user_1)

        assert isinstance(created_user_1.id, str)
        assert created_user_1.id == '1'
        assert created_user_1.name == user_1.name
        assert created_user_1.email == user_1.email
        assert created_user_1.password == user_1.password
        assert isinstance(created_user_1.created_at, datetime)
        assert created_user_1.created_at == datetime(
            2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc
        )

        user_2 = User(
            name='User 2',
            email='user2@test.com',
            password='123456789',
        )

        created_user_2 = await fake_user_repository.create(user_2)

        assert isinstance(created_user_2.id, str)
        assert created_user_2.id == '2'
        assert created_user_2.name == user_2.name
        assert created_user_2.email == user_2.email
        assert created_user_2.password == user_2.password
        assert isinstance(created_user_2.created_at, datetime)
        assert created_user_2.created_at == datetime(
            2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc
        )
