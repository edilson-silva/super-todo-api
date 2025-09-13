from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    async def async_hash(self, password: str) -> str:
        """
        Hash a password.

        :param password: The plain text password to hash.

        :return: The hashed password.
        """
        pass

    @abstractmethod
    async def async_check(self, password: str, hashed_password: str) -> bool:
        """
        Check if password and hashed_password are the same.

        :param password: The plain text password.
        :param password: The hashed password.

        :return: True if passowrd are equal and False otherwise.
        """
        pass
