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

    async def test_find_by_valid_email_should_return_user(
        self,
        user_repository: UserRepository,
        admin_user: User,
    ):
        found_user = await user_repository.find_by_email(admin_user.email)

        assert isinstance(found_user, User)
        assert found_user.id == admin_user.id
        assert found_user.email == admin_user.email
        assert found_user.name == admin_user.name
        assert found_user.password == admin_user.password
        assert found_user.role == admin_user.role
        assert found_user.company_id == admin_user.company_id
        assert found_user.avatar == admin_user.avatar
        assert found_user.created_at == admin_user.created_at
        assert found_user.updated_at == admin_user.updated_at

    async def test_find_by_invalid_email_should_return_none(
        self, user_repository: UserRepository
    ):
        found_user = await user_repository.find_by_email(
            'invalid_email@example.com'
        )

        assert found_user is None

    async def test_find_by_valid_id_should_return_user(
        self,
        user_repository: UserRepository,
        admin_user: User,
    ):
        found_user = await user_repository.find_by_id(
            str(admin_user.id), str(admin_user.company_id)
        )

        assert isinstance(found_user, User)
        assert found_user.id == admin_user.id
        assert found_user.email == admin_user.email
        assert found_user.name == admin_user.name
        assert found_user.password == admin_user.password
        assert found_user.role == admin_user.role
        assert found_user.company_id == admin_user.company_id
        assert found_user.avatar == admin_user.avatar
        assert found_user.created_at == admin_user.created_at
        assert found_user.updated_at == admin_user.updated_at
