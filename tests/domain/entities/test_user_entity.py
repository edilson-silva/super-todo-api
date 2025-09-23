from datetime import datetime, timezone
from uuid import UUID

from src.domain.entities.user_entity import User, UserRole


class TestUserEntity:
    def test_user_entity_create_with_default_attributes(self):
        user_name = 'Test User'
        user_email = 'test@example.com'
        user_password = '123456789'
        user_role = UserRole.ADMIN

        user = User(
            name=user_name,
            email=user_email,
            password=user_password,
            role=user_role,
        )

        assert user.id is not None
        assert isinstance(user.id, UUID)
        assert user.name == user_name
        assert user.email == user_email
        assert user.password == user_password
        assert user.role == user_role
        assert user.avatar == ''
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)
        assert user.created_at.tzinfo is not None
        assert user.created_at.tzinfo == timezone.utc

    def test_user_entity_create_with_all_attributes(self):
        user_id = 'custom-id'
        user_name = 'Test User'
        user_email = 'test@example.com'
        user_password = '123456789'
        user_role = UserRole.USER
        user_avatar = 'custom-avatar'
        user_created_at = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        user = User(
            id=user_id,
            name=user_name,
            email=user_email,
            password=user_password,
            role=user_role,
            avatar=user_avatar,
            created_at=user_created_at,
        )

        assert user.id == user_id
        assert user.name == user_name
        assert user.email == user_email
        assert user.password == user_password
        assert user.role == user_role
        assert user.avatar == user_avatar
        assert user.created_at == user_created_at
        assert isinstance(user.created_at, datetime)
