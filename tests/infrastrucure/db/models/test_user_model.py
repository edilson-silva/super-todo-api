from datetime import datetime, timezone

from uuid_extensions import uuid7str

from src.infrastructure.db.models.user_model import UserModel

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


class TestUserModel:
    def test_valid_info_should_create_a_model(self, admin_user_info: dict):
        user_info = {
            'id': uuid7str(),
            'name': admin_user_info['name'],
            'email': admin_user_info['email'],
            'password': admin_user_info['password'],
            'role': admin_user_info['role'],
            'avatar': 'http://example.com/avatar.png',
            'company_id': uuid7str(),
            'created_at': mock_datetime,
            'updated_at': mock_datetime,
        }

        model = UserModel(**user_info)

        assert model.id == user_info['id']
        assert model.name == user_info['name']
        assert model.email == user_info['email']
        assert model.password == user_info['password']
        assert model.role == user_info['role']
        assert model.avatar == user_info['avatar']
        assert model.company_id == user_info['company_id']
        assert model.created_at == user_info['created_at']
        assert model.updated_at == user_info['updated_at']
