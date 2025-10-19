import pytest

from src.domain.entities.company_entity import Company
from src.domain.repositories.company_repository import CompanyRepository


@pytest.mark.asyncio
class TestCompanyRepositorySQLAlchemy:
    async def test_valid_info_should_create_company(
        self, company_repository: CompanyRepository
    ):
        company = Company(name='Test Company')

        created_company = await company_repository.create(company)

        assert created_company is not None
        assert created_company.id == str(company.id)
        assert created_company.name == company.name
