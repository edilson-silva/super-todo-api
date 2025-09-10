import aiobcrypt
from aiobcrypt import hashpw

from src.domain.security.password_hasher import PasswordHasher


class PasswordHasherBcrypt(PasswordHasher):
    async def async_hash(self, password: str) -> str:
        """
        Hash a password using bcrypt.

        :param password: The plain text password to hash.

        :return: The hashed password.
        """
        salt: bytes = await aiobcrypt.gensalt(10)
        hashed_password: bytes = await hashpw(password.encode(), salt)

        return hashed_password.decode()
