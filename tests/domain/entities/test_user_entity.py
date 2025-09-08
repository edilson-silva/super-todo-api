from datetime import datetime, timezone

from src.domain.entities.user_entity import User


class TestUserEntity:
    def test_user_entity_create_with_default_attributes(self):
        user_name = 'Test User'
        user_email = 'test@example.com'
        user_password = '123456789'

        user = User(
            name=user_name,
            email=user_email,
            password=user_password,
        )

        assert user.id is not None
        assert isinstance(user.id, str)
        assert user.name == user_name
        assert user.email == user_email
        assert user.password == user_password
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)
        assert user.created_at.tzinfo is not None
        assert user.created_at.tzinfo == timezone.utc
