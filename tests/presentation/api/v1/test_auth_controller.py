import pytest
from fastapi import status
from httpx import AsyncClient

from src.core.settings import settings


@pytest.fixture(scope='class')
def signup_user_info():
    return {
        'company_name': 'Test Company',
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
    async def test_missing_request_params_should_return_unprocessable_error(
        self, client: AsyncClient
    ):
        response = await client.post('/auth/signup', json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {
            'detail': [
                {
                    'type': 'missing',
                    'loc': ['body', 'company_name'],
                    'msg': 'Field required',
                    'input': {},
                },
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

    async def test_signup_user_info_should_return_success(
        self, client: AsyncClient, signup_user_info: dict
    ):
        response = await client.post('/auth/signup', json=signup_user_info)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.text == 'null'

    async def test_existing_user_info_should_return_conflict_error(
        self, client: AsyncClient, signup_user_info: dict
    ):
        response1 = await client.post('/auth/signup', json=signup_user_info)

        assert response1.status_code == status.HTTP_201_CREATED
        assert response1.text == 'null'

        response2 = await client.post('/auth/signup', json=signup_user_info)

        assert response2.status_code == status.HTTP_409_CONFLICT
        assert response2.json() == {'detail': 'Conflict'}


class TestAuthSigninController:
    async def test_missing_request_params_should_return_unprocessable_error(
        self, client: AsyncClient
    ):
        response = await client.post('/auth/signin', data={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {
            'detail': [
                {
                    'type': 'missing',
                    'loc': ['query', 'email'],
                    'msg': 'Field required',
                    'input': None,
                },
                {
                    'type': 'missing',
                    'loc': ['query', 'password'],
                    'msg': 'Field required',
                    'input': None,
                },
            ]
        }

    async def test_valid_user_credentials_should_return_success_with_token(
        self,
        client: AsyncClient,
        signup_user_info: dict,
        signin_user_info: dict,
    ):
        signup_response = await client.post(
            '/auth/signup', json=signup_user_info
        )

        print('SI:', signin_user_info)

        assert signup_response.status_code == status.HTTP_201_CREATED

        signin_response = await client.post(
            '/auth/signin', data=signin_user_info
        )

        assert signin_response.status_code == status.HTTP_200_OK

        access_token = signin_response.json().get('access_token')

        assert isinstance(access_token, dict)
        assert access_token != {}
        assert 'token' in access_token
        assert 'token_type' in access_token
        assert access_token['token'] != ''
        assert access_token['token_type'] == settings.ACCESS_TOKEN_TYPE

    async def test_invalid_user_credentials_should_return_unauthorized_error(
        self,
        client: AsyncClient,
    ):
        response = await client.post('/auth/signin', data=signin_user_info)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorized'}
