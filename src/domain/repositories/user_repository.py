from abc import ABC, abstractmethod
from typing import List

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
    async def find_by_id(self, user_id: str, company_id: str) -> User | None:
        """
        Find a user baed on its id.

        :param user_id: Serch id.
        :param company_id: Id of the company the user belongs to.

        :return: The user if found and None otherwise.
        """
        pass

    @abstractmethod
    async def find_all(
        self, company_id: str, limit: int, offset: int
    ) -> List[User]:
        """
        Find all company users.

        :param company_id: The company id to filter users.
        :param limit: Maximum number of users returned.
        :param offset: Number of users ignored in the search.

        :return: The list of found users.
        """
        pass

    @abstractmethod
    async def delete_by_id(self, user_id: str, company_id: str) -> None:
        """
        Delete a user baed on its id.

        :param user_id: Serch id.
        :param company_id: Id of the company the user belongs to.

        :return: None.
        """
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """
        Update a user baed on its id.

        :param user: User entity to update.

        :return: The updated User entity.
        """
        pass
