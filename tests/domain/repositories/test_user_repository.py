from dataclasses import replace
from datetime import datetime, timezone
from uuid import UUID

import pytest
from freezegun import freeze_time
from uuid_extensions import uuid7

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
            company_id=uuid7(),
        )

        created_user = await user_repository.create(user)

        assert isinstance(created_user.id, str)
        assert created_user.id != ''
        assert created_user.name == user.name
        assert created_user.email == user.email
        assert created_user.password == user.password
        assert created_user.role == user.role
        assert created_user.avatar == user.avatar
        assert isinstance(user.company_id, UUID)
        assert created_user.company_id == user.company_id
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
    async def test_should_find_user_by_email(
        self, user_repository: UserRepository
    ):
        user = User(
            name='User 1',
            email='user1@test.com',
            password='123456789',
            role=UserRole.ADMIN,
            company_id=uuid7(),
        )

        created_user = await user_repository.create(user)

        found_user = await user_repository.find_by_email(
            str(created_user.email)
        )

        assert found_user
        assert isinstance(found_user.id, str)
        assert created_user.id == found_user.id
        assert created_user.name == found_user.name
        assert created_user.email == found_user.email
        assert created_user.password == found_user.password
        assert created_user.role == found_user.role
        assert created_user.avatar == found_user.avatar
        assert created_user.company_id == user.company_id
        assert created_user.created_at == found_user.created_at

    @freeze_time(mock_datetime)
    async def test_should_list_users(self, user_repository: UserRepository):
        user_1 = User(
            name='User 1',
            email='user1@test.com',
            password='123456789',
            role=UserRole.ADMIN,
            company_id=uuid7(),
        )
        user_2 = User(
            name='User 2',
            email='user2@test.com',
            password='123456789',
            role=UserRole.USER,
            avatar='custom-avatar',
            company_id=uuid7(),
        )

        created_user_1 = await user_repository.create(user_1)
        created_user_2 = await user_repository.create(user_2)

        found_users = await user_repository.find_all(10, 0)

        assert len(found_users) == 2

        found_user_1, found_user_2 = found_users

        assert found_user_1.id == created_user_1.id
        assert found_user_1.name == created_user_1.name
        assert found_user_1.email == created_user_1.email
        assert found_user_1.password == created_user_1.password
        assert found_user_1.role == created_user_1.role
        assert found_user_1.avatar == created_user_1.avatar
        assert found_user_1.company_id == created_user_1.company_id
        assert found_user_1.created_at == created_user_1.created_at

        assert found_user_2.id == created_user_2.id
        assert found_user_2.name == created_user_2.name
        assert found_user_2.email == created_user_2.email
        assert found_user_2.password == created_user_2.password
        assert found_user_2.role == created_user_2.role
        assert found_user_2.avatar == created_user_2.avatar
        assert found_user_2.company_id == created_user_2.company_id
        assert found_user_2.created_at == created_user_2.created_at

    @freeze_time(mock_datetime)
    async def test_should_update_user(self, user_repository: UserRepository):
        user_create = User(
            name='User 1',
            email='user1@test.com',
            password='123456789',
            role=UserRole.ADMIN,
            company_id=uuid7(),
        )

        await user_repository.create(user_create)

        user_update = replace(
            user_create,
            name='User updated',
            email='user@updated.com',
            password='updated_password',
            role=UserRole.USER,
        )

        updated_user = await user_repository.update(user_update)

        assert user_update.id == updated_user.id
        assert user_update.name == updated_user.name
        assert user_update.email == updated_user.email
        assert user_update.password == updated_user.password
        assert user_update.role == updated_user.role
        assert user_update.avatar == updated_user.avatar
        assert user_update.company_id == updated_user.company_id
        assert user_update.created_at == updated_user.created_at

    @freeze_time(mock_datetime)
    async def test_should_delete_a_user(self, user_repository: UserRepository):
        user = User(
            name='User 1',
            email='user1@test.com',
            password='123456789',
            role=UserRole.ADMIN,
            company_id=uuid7(),
        )

        created_user = await user_repository.create(user)

        response = await user_repository.delete_by_id(str(created_user.id))

        assert response is None
