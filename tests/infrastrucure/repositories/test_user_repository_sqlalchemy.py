import pytest
from uuid_extensions import uuid7str

from src.domain.entities.user_entity import User
from src.domain.repositories.user_repository import UserRepository


@pytest.mark.asyncio
class TestUserRepositorySQLAlchemy:
    async def test_valid_info_should_create_user(
        self, user_repository: UserRepository, admin_user_info: dict
    ):
        user = User(
            name=admin_user_info['name'],
            email=admin_user_info['email'],
            password=admin_user_info['password'],
            role=admin_user_info['role'],
            company_id=uuid7str(),
            avatar='',
        )

        created_user = await user_repository.create(user)

        assert isinstance(created_user, User)
        assert created_user.id == str(user.id)
        assert created_user.name == user.name
        assert created_user.email == user.email
        assert created_user.password == user.password
        assert created_user.role == user.role
        assert created_user.company_id == str(user.company_id)
        assert created_user.avatar == user.avatar
