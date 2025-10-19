from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.company_entity import Company
from src.domain.entities.user_entity import User
from src.domain.exceptions.exceptions import CannotOperateException
from src.domain.repositories.company_repository import CompanyRepository
from src.infrastructure.repositories.company_repository_sqlalchemy import (
    CompanyRepositorySQLAlchemy,
)


@pytest.mark.asyncio
class TestCompanyRepositorySQLAlchemy:
    async def test_valid_info_should_create_company(
        self, company_repository: CompanyRepository
    ):
        company = Company(name='Test Company')

        created_company = await company_repository.create(company)

        assert isinstance(created_company, Company)
        assert created_company.id == str(company.id)
        assert created_company.name == company.name

    async def test_find_by_valid_name_should_return_company(
        self,
        company_repository: CompanyRepository,
        admin_user: User,
        admin_user_info: dict,
    ):
        company_name = admin_user_info['company_name']

        found_company = await company_repository.find_by_name(company_name)

        assert isinstance(found_company, Company)
        assert found_company.id is not None
        assert isinstance(found_company.id, str)
        assert found_company.name == company_name

    async def test_create_company_failure(self):
        company = Company(name='Test Company')

        # Fake session that raises SQLAlchemyError on add
        fake_session = MagicMock()
        fake_session.add.side_effect = SQLAlchemyError('DB Error')
        fake_session.commit = AsyncMock()

        company_repository = CompanyRepositorySQLAlchemy(fake_session)

        with pytest.raises(CannotOperateException) as exc_info:
            await company_repository.create(company)

        assert str(exc_info.value) == 'Cannot operate: Try again later'
