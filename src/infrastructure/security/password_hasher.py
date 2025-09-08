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
