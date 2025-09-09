from datetime import datetime, timezone
from typing import List

import pytest

from src.domain.entities.user_entity import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.security.password_hasher import PasswordHasher


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

        async def get_by_email(self, email: str) -> User | None:
            for user in self.users:
                if user.email == email:
                    return user
            return None

    return FakeUserRepository()


@pytest.fixture
def fake_password_hasher() -> PasswordHasher:
    class FakePasswordHasher(PasswordHasher):
        async def async_hash(self, password: str) -> str:
            return f'hashed_{password}'

    return FakePasswordHasher()
