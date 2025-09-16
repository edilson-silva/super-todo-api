import pytest
from fastapi import status
from httpx import Client


@pytest.fixture(scope='class')
def new_user_info():
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': '123456789',
    }


class TestAuthSignupController:
    def test_missing_request_params_should_return_error(
        self, client_with_mock_deps: Client
    ):
        response = client_with_mock_deps.post('/auth/signup', json={})

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

    def test_new_user_info_should_return_success(
        self, client_with_mock_deps: Client, new_user_info: dict
    ):
        response = client_with_mock_deps.post(
            '/auth/signup', json=new_user_info
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.text == 'null'

    def test_existing_user_info_should_return_conflict(
        self, client_with_mock_deps: Client, new_user_info: dict
    ):
        response1 = client_with_mock_deps.post(
            '/auth/signup', json=new_user_info
        )

        assert response1.status_code == status.HTTP_201_CREATED
        assert response1.text == 'null'

        response2 = client_with_mock_deps.post(
            '/auth/signup', json=new_user_info
        )

        assert response2.status_code == status.HTTP_409_CONFLICT
        assert response2.json() == {'detail': 'Conflict'}


class TestAuthSigninController:
    def test_missing_request_params_should_return_error(
        self, client_with_mock_deps: Client
    ):
        response = client_with_mock_deps.post('/auth/signin', json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {
            'detail': [
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
