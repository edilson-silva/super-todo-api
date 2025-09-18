from abc import ABC, abstractmethod

from src.domain.entities.user_entity import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Create a new user to the repository.

        :param user: User entity to create.

        :return: The created User entity.
        """
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        """
        Find a user baed on its email.

        :param email: Serch email.

        :return: The user if found and None otherwise.
        """
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None:
        """
        Find a user baed on its id.

        :param user_id: Serch id.

        :return: The user if found and None otherwise.
        """
        pass
