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

    async def test_should_check_and_return_true_for_a_valid_password(
        self, password_hasher: PasswordHasher
    ):
        password = '123456789'
        hashed_password = (
            '$2b$10$zZvbpDt7Y2puEr50dK65x.LKRS63PrxL1L6YaW9p5ChgLOcBQrV9S'
        )

        valid = await password_hasher.async_check(password, hashed_password)

        assert valid
