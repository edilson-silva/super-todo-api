from abc import ABC, abstractmethod

from src.domain.entities.user_entity import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Create a new user to the repository.
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email.
        """
        pass
