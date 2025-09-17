import pytest
from fastapi import status
from httpx import Client

from src.domain.entities.user_role import UserRole


@pytest.fixture(scope='class')
def create_user_info():
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': '123456789',
        'role': UserRole.USER,
    }


class TestUserController:
    def test_missing_request_params_should_return_unprocessable_error(
        self, client_with_mock_deps: Client
    ):
        response = client_with_mock_deps.post('/users', json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {
            'detail': [
                {
                    'type': 'missing',
                    'loc': ['body', 'name'],
                    'msg': 'Field required',
                    'input': {},
                },
                {
                    'type': 'missing',
                    'loc': ['body', 'email'],
                    'msg': 'Field required',
                    'input': {},
                },
                {
                    'type': 'missing',
                    'loc': ['body', 'password'],
                    'msg': 'Field required',
                    'input': {},
                },
            ]
        }

    def test_create_user_info_should_return_success(
        self, client_with_mock_deps: Client, create_user_info: dict
    ):
        response = client_with_mock_deps.post('/users', json=create_user_info)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            'id': '1',
            'name': 'Test User',
            'email': 'test@example.com',
            'role': 'user',
            'avatar': '',
            'created_at': '2025-01-01T00:00:00Z',
        }

    def test_existing_user_info_should_return_bad_request_error(
        self, client_with_mock_deps: Client, create_user_info: dict
    ):
        response1 = client_with_mock_deps.post('/users', json=create_user_info)

        assert response1.status_code == status.HTTP_201_CREATED
        assert response1.json() == {
            'id': '1',
            'name': 'Test User',
            'email': 'test@example.com',
            'role': 'user',
            'avatar': '',
            'created_at': '2025-01-01T00:00:00Z',
        }

        response2 = client_with_mock_deps.post('/users', json=create_user_info)

        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert response2.json() == {'detail': 'Bad Request'}
