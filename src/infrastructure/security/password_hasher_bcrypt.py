import aiobcrypt
from aiobcrypt import checkpw, hashpw

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

    async def async_check(self, password: str, hashed_password: str) -> bool:
        """
        Check if password and hashed_password are the same.

        :param password: The plain text password.
        :param password: The hashed password.

        :return: True if passowrd are equal and False otherwise.
        """
        return await checkpw(password.encode(), hashed_password.encode())
