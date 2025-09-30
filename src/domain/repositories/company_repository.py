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
