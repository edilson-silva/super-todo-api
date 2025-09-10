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
