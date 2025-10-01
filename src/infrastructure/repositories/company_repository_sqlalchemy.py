from collections.abc import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.company_entity import Company
from src.domain.exceptions.exceptions import CannotOperateException
from src.domain.repositories.company_repository import CompanyRepository
from src.infrastructure.db.models.company_model import CompanyModel


class CompanyRepositorySQLAlchemy(CompanyRepository):
    def __init__(self, session: AsyncGenerator[AsyncSession, None]):
        self.session = session

    async def create(self, company: Company) -> Company | None:
        """
        Create a new company to the repository.

        :param company: Company entity to create.

        :return: The created Company entity or None otherwise.
        """
        try:
            company_model = CompanyModel(
                id=company.id,
                name=company.name,
                type=company.type,
                max_users=company.max_users,
                created_at=company.created_at,
                updated_at=company.updated_at,
            )
            self.session.add(company_model)
            await self.session.commit()
            await self.session.refresh(company_model)

            company.id = str(company.id)

            return company
        except SQLAlchemyError:
            raise CannotOperateException()

    async def find_by_name(self, name: str) -> Company | None:
        """
        Find a company based on its name.

        :param name: Search name.

        :return: The company if found and None otherwise.
        """
        stmt = select(CompanyModel).filter(CompanyModel.name == name)
        query = await self.session.execute(stmt)
        result = query.scalar_one_or_none()

        if result:
            return Company(
                id=str(result.id),
                name=result.name,
                type=result.type,
                max_users=result.max_users,
                created_at=result.created_at,
                updated_at=result.updated_at,
            )
