from abc import ABC, abstractmethod

from src.domain.entities.company_entity import Company


class CompanyRepository(ABC):
    @abstractmethod
    async def create(self, company: Company) -> Company | None:
        """
        Create a new company to the repository.

        :param company: Company entity to create.

        :return: The created Company entity or None otherwise.
        """
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Company | None:
        """
        Find a company based on its name.

        :param name: Search name.

        :return: The company if found and None otherwise.
        """
        pass
