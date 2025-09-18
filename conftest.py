from datetime import datetime, timezone
from typing import Generator, List

import pytest
from fastapi.testclient import TestClient
from httpx import Client

from src.application.dtos.security.token_generator_decode_dto import (
    TokenGeneratorDecodeOutputDTO,
)
from src.application.dtos.security.token_generator_encode_dto import (
    TokenGeneratorEncodeInputDTO,
)
from src.application.usecases.auth.auth_signin_usecase import AuthSigninUseCase
from src.application.usecases.auth.auth_signup_usecase import AuthSignupUseCase
from src.application.usecases.user.user_create_usecase import UserCreateUseCase
from src.application.usecases.user.user_get_usecase import UserGetUseCase
from src.core.container import (
    get_auth_signin_use_case,
    get_auth_signup_use_case,
    get_password_hasher,
    get_user_create_use_case,
    get_user_get_use_case,
    get_user_repository,
)
from src.core.settings import settings
from src.domain.entities.user_entity import User, UserRole
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher
from src.domain.security.token_generator import TokenGenerator
from src.main import app


@pytest.fixture
def fake_user_repository() -> UserRepository:
    class FakeUserRepository(UserRepository):
        def __init__(self):
            self.users: List[User] = []

        async def create(self, user: User) -> User:
            user.id = str(len(self.users) + 1)
            user.created_at = datetime(
                2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc
            )
            self.users.append(user)
            return user

        async def find_by_email(self, email: str) -> User | None:
            for user in self.users:
                if user.email == email:
                    return user

        async def find_by_id(self, user_id: str) -> User | None:
            for user in self.users:
                if user.id == user_id:
                    return user

    return FakeUserRepository()


@pytest.fixture
def fake_password_hasher() -> PasswordHasher:
    class FakePasswordHasher(PasswordHasher):
        async def async_hash(self, password: str) -> str:
            return f'hashed_{password}'

        async def async_check(self, password, hashed_password) -> bool:
            return f'hashed_{password}' == hashed_password

    return FakePasswordHasher()


@pytest.fixture
def fake_token_generator() -> TokenGenerator:
    class FakeTokenGenerator(TokenGenerator):
        def __init__(self):
            self.token_type = settings.ACCESS_TOKEN_TYPE

        async def async_encode(
            self, payload: TokenGeneratorEncodeInputDTO
        ) -> str:
            return f'{self.token_type} fake_token'

        async def async_decode(
            self, access_token: str
        ) -> TokenGeneratorDecodeOutputDTO:
            return TokenGeneratorDecodeOutputDTO(
                user_id='1', user_role=UserRole.ADMIN
            )

    return FakeTokenGenerator()


@pytest.fixture
def sample_user() -> User:
    user = User(
        name='Test User',
        email='test@example.com',
        password='123456789',
        role=UserRole.ADMIN,
    )
    return user


@pytest.fixture
def client_with_mock_deps(
    fake_user_repository, fake_password_hasher, fake_token_generator
) -> Generator[Client, None, None]:
    def fake_auth_signup_use_case() -> AuthSignupUseCase:
        return AuthSignupUseCase(fake_user_repository, fake_password_hasher)

    def fake_auth_signin_use_case() -> AuthSigninUseCase:
        return AuthSigninUseCase(
            fake_user_repository, fake_password_hasher, fake_token_generator
        )

    def fake_user_create_use_case() -> UserCreateUseCase:
        return UserCreateUseCase(fake_user_repository, fake_password_hasher)

    def fake_user_get_use_case() -> UserGetUseCase:
        return UserGetUseCase(fake_user_repository)

    # Overide dependencies before test
    app.dependency_overrides[get_user_repository] = fake_user_repository
    app.dependency_overrides[get_password_hasher] = fake_password_hasher
    app.dependency_overrides[get_auth_signup_use_case] = (
        fake_auth_signup_use_case
    )
    app.dependency_overrides[get_auth_signin_use_case] = (
        fake_auth_signin_use_case
    )
    app.dependency_overrides[get_user_create_use_case] = (
        fake_user_create_use_case
    )
    app.dependency_overrides[get_user_get_use_case] = fake_user_get_use_case

    yield TestClient(app)

    # Cleanup overrides dependencies after test
    app.dependency_overrides.clear()
