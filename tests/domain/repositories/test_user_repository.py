from datetime import datetime, timezone

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
    async def test_should_create_a_user(self, user_repository: UserRepository):
        user = User(
            name='User 1',
            email='user1@test.com',
            password='123456789',
            role=UserRole.ADMIN,
        )

        created_user = await user_repository.create(user)

        assert isinstance(created_user.id, str)
        assert created_user.id != ''
        assert created_user.name == user.name
        assert created_user.email == user.email
        assert created_user.password == user.password
        assert created_user.role == user.role
        assert created_user.avatar == user.avatar
        assert isinstance(created_user.created_at, datetime)
        assert created_user.created_at == mock_datetime

        found_user = await user_repository.find_by_id(str(created_user.id))

        assert found_user
        assert isinstance(found_user.id, str)
        assert created_user.id == found_user.id
        assert created_user.name == found_user.name
        assert created_user.email == found_user.email
        assert created_user.password == found_user.password
        assert created_user.role == found_user.role
        assert created_user.avatar == found_user.avatar
        assert created_user.created_at == found_user.created_at

    @freeze_time(mock_datetime)
    async def test_should_list_users(self, user_repository: UserRepository):
        user_1 = User(
            name='User 1',
            email='user1@test.com',
            password='123456789',
            role=UserRole.ADMIN,
        )

        created_user_1 = await user_repository.create(user_1)

        assert isinstance(created_user_1.id, str)
        assert created_user_1.id != ''
        assert created_user_1.name == user_1.name
        assert created_user_1.email == user_1.email
        assert created_user_1.password == user_1.password
        assert created_user_1.role == user_1.role
        assert created_user_1.avatar == user_1.avatar
        assert isinstance(created_user_1.created_at, datetime)
        assert created_user_1.created_at == mock_datetime

        user_2 = User(
            name='User 2',
            email='user2@test.com',
            password='123456789',
            role=UserRole.USER,
            avatar='custom-avatar',
        )

        created_user_2 = await user_repository.create(user_2)

        assert isinstance(created_user_2.id, str)
        assert created_user_2.id != ''
        assert created_user_2.name == user_2.name
        assert created_user_2.email == user_2.email
        assert created_user_2.password == user_2.password
        assert created_user_2.role == user_2.role
        assert created_user_2.avatar == user_2.avatar
        assert isinstance(created_user_2.created_at, datetime)
        assert created_user_2.created_at == mock_datetime

        found_users = await user_repository.find_all(10, 0)

        assert len(found_users) == 2

        found_user_1, found_user_2 = found_users

        assert found_user_1.id == created_user_1.id
        assert found_user_1.name == created_user_1.name
        assert found_user_1.email == created_user_1.email
        assert found_user_1.password == created_user_1.password
        assert found_user_1.role == created_user_1.role
        assert found_user_1.avatar == created_user_1.avatar
        assert found_user_1.created_at == created_user_1.created_at

        assert found_user_2.id == created_user_2.id
        assert found_user_2.name == created_user_2.name
        assert found_user_2.email == created_user_2.email
        assert found_user_2.password == created_user_2.password
        assert found_user_2.role == created_user_2.role
        assert found_user_2.avatar == created_user_2.avatar
        assert found_user_2.created_at == created_user_2.created_at
