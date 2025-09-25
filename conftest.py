from collections.abc import AsyncGenerator
from datetime import datetime, timezone
from typing import List

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.application.dtos.security.token_generator_decode_dto import (
    TokenGeneratorDecodeOutputDTO,
)
from src.application.dtos.security.token_generator_encode_dto import (
    TokenGeneratorEncodeInputDTO,
)
from src.core.settings import settings
from src.domain.entities.user_entity import User, UserRole
from src.domain.repositories.user_repository import UserRepository
from src.domain.security.password_hasher import PasswordHasher
from src.domain.security.token_generator import TokenGenerator
from src.infrastructure.db.session import Base, get_db
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

        async def find_all(self) -> List[User]:
            return self.users

        async def delete_by_id(self, user_id: str) -> None:
            self.users = list(
                filter(lambda u: str(u.id) != user_id, self.users)
            )

        async def update(self, user: User) -> User:
            for i in range(len(self.users)):
                if self.users[i].id == user.id:
                    self.users[i].name = user.name
                    self.users[i].password = user.password
                    self.users[i].role = user.role
                    self.users[i].avatar = user.avatar
                    self.users[i].created_at = user.created_at

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
def sample_user_info() -> dict:
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': '123456789',
        'role': UserRole.ADMIN,
    }


@pytest.fixture
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')

    AsyncSesssionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSesssionLocal() as session:
        yield session

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def client(get_db_session) -> AsyncGenerator[AsyncClient, None]:
    def override_get_db_session():
        yield get_db_session

    app.dependency_overrides[get_db] = override_get_db_session

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport, base_url='http://test', follow_redirects=True
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def datetime_to_web_iso():
    def convert_date(date: datetime) -> str:
        return date.isoformat().replace('+00:00', 'Z')

    return convert_date
