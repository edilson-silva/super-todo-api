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


class TestUserCreateController:
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


class TestUserGetController:
    def test_valid_id_should_return_success(
        self, client_with_mock_deps: Client, create_user_info: dict
    ):
        user_create_response = client_with_mock_deps.post(
            '/users', json=create_user_info
        )

        assert user_create_response.status_code == status.HTTP_201_CREATED

        user_created = user_create_response.json()

        user_get_response = client_with_mock_deps.get(
            f'/users/{user_created["id"]}'
        )

        assert user_get_response.status_code == status.HTTP_200_OK

        user_found = user_get_response.json()

        assert user_found['id'] == user_created['id']
        assert user_found['name'] == user_created['name']
        assert user_found['email'] == user_created['email']
        assert user_found['role'] == user_created['role']
        assert user_found['avatar'] == user_created['avatar']
        assert user_found['created_at'] == user_created['created_at']

    def test_invalid_id_should_return_not_found_error(
        self, client_with_mock_deps: Client, create_user_info: dict
    ):
        response = client_with_mock_deps.get('/users/invalid-id')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Not Found'}


class TestUserListController:
    def test_should_return_success(
        self, client_with_mock_deps: Client, create_user_info: dict
    ):
        user_create_response = client_with_mock_deps.post(
            '/users', json=create_user_info
        )

        assert user_create_response.status_code == status.HTTP_201_CREATED

        user_created = user_create_response.json()

        user_list_response = client_with_mock_deps.get('/users')

        assert user_list_response.status_code == status.HTTP_200_OK

        users = user_list_response.json()

        assert isinstance(users, dict)
        assert len(users['data']) == 1

        user = users['data'][0]

        assert user['id'] == user_created['id']
        assert user['name'] == user_created['name']
        assert user['email'] == user_created['email']
        assert user['role'] == user_created['role']
        assert user['avatar'] == user_created['avatar']
        assert user['created_at'] == user_created['created_at']
