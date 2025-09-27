import pytest

from src.domain.security.password_hasher import PasswordHasher


@pytest.mark.asyncio
class TestPasswordHasher:
    async def test_should_hash_a_password(
        self, password_hasher: PasswordHasher
    ):
        password = '123456789'
        hashed_password = await password_hasher.async_hash(password)

        assert isinstance(hashed_password, str)
        assert hashed_password != ''
