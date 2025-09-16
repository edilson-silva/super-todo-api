import pytest
from fastapi import status
from httpx import Client


@pytest.fixture(scope='class')
def signup_user_info():
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': '123456789',
    }


@pytest.fixture(scope='class')
def signin_user_info():
    return {
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

    def test_signup_user_info_should_return_success(
        self, client_with_mock_deps: Client, signup_user_info: dict
    ):
        response = client_with_mock_deps.post(
            '/auth/signup', json=signup_user_info
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.text == 'null'

    def test_existing_user_info_should_return_conflict(
        self, client_with_mock_deps: Client, signup_user_info: dict
    ):
        response1 = client_with_mock_deps.post(
            '/auth/signup', json=signup_user_info
        )

        assert response1.status_code == status.HTTP_201_CREATED
        assert response1.text == 'null'

        response2 = client_with_mock_deps.post(
            '/auth/signup', json=signup_user_info
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

    def test_valid_user_credentials_should_return_success_with_access_token(
        self,
        client_with_mock_deps: Client,
        signup_user_info: dict,
        signin_user_info: dict,
    ):
        signup_response = client_with_mock_deps.post(
            '/auth/signup', json=signup_user_info
        )

        assert signup_response.status_code == status.HTTP_201_CREATED

        signin_response = client_with_mock_deps.post(
            '/auth/signin', json=signin_user_info
        )

        assert signin_response.status_code == status.HTTP_200_OK
        assert signin_response.json() == {
            'access_token': 'Bearer fake_token',
        }
