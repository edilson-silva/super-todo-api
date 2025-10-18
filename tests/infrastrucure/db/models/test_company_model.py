from datetime import datetime, timezone

import pytest
from uuid_extensions import uuid7str

from src.domain.entities.company_type import CompanyType
from src.infrastructure.db.models.company_model import CompanyModel

mock_datetime = datetime(
    2025,
    1,
    1,
    0,
    0,
    0,
    0,
    timezone.utc,
)


class TestCompanyModel:
    def test_valid_info_should_create_a_model(self):
        company_info = {
            'id': uuid7str(),
            'name': 'Test Company',
            'type': CompanyType.PRO,
            'max_users': 10,
            'created_at': mock_datetime,
            'updated_at': mock_datetime,
        }

        model = CompanyModel(**company_info)

        assert model.id == company_info['id']
        assert model.name == company_info['name']
        assert model.type == company_info['type']
        assert model.max_users == company_info['max_users']
        assert model.created_at == company_info['created_at']
        assert model.updated_at == company_info['updated_at']

    def test_invalid_max_users_should_raise_value_error(self):
        company_info = {
            'id': uuid7str(),
            'name': 'Test Company',
            'type': CompanyType.PRO,
            'max_users': 0,
            'created_at': mock_datetime,
            'updated_at': mock_datetime,
        }

        with pytest.raises(ValueError) as exc_info:
            CompanyModel(**company_info)

        assert str(exc_info.value) == (
            'Max users value must be greater than 0, but got 0'
        )
