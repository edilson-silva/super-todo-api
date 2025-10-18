from fastapi import status
from httpx import AsyncClient

from src.core.settings import settings
from src.domain.entities.user_entity import User


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
        self, client: AsyncClient, admin_user_info: dict
    ):
        response = await client.post('/auth/signup', json=admin_user_info)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.text == 'null'

    async def test_existing_user_info_should_return_conflict_error(
        self, client: AsyncClient, admin_user: User, admin_user_info: dict
    ):
        response = await client.post('/auth/signup', json=admin_user_info)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'detail': 'Bad Request'}

    async def test_existing_company_name_should_return_conflict_error(
        self, client: AsyncClient, admin_user: User, admin_user_info: dict
    ):
        await client.post('/auth/signup', json=admin_user_info)

        new_user = {
            'company_name': admin_user_info['company_name'],
            'name': 'Another User',
            'email': 'anotheruser@example.com',
            'password': 'AnotherPassword123!',
        }

        response = await client.post('/auth/signup', json=new_user)

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {'detail': 'Company already registered'}


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
                    'loc': ['body', 'username'],
                    'msg': 'Field required',
                    'input': None,
                },
                {
                    'type': 'missing',
                    'loc': ['body', 'password'],
                    'msg': 'Field required',
                    'input': None,
                },
            ]
        }

    async def test_valid_user_credentials_should_return_success_with_token(
        self, client: AsyncClient, admin_user: User, admin_user_info: dict
    ):
        response = await client.post(
            '/auth/signin',
            data={
                'username': admin_user_info['email'],
                'password': admin_user_info['password'],
            },
        )

        assert response.status_code == status.HTTP_200_OK

        access_token = response.json()

        assert isinstance(access_token, dict)
        assert access_token != {}
        assert 'access_token' in access_token
        assert 'token_type' in access_token
        assert access_token['access_token'] != ''
        assert access_token['token_type'] == settings.ACCESS_TOKEN_TYPE

    async def test_invalid_user_credentials_should_return_unauthorized_error(
        self, client: AsyncClient, admin_user: User, admin_user_info: dict
    ):
        response = await client.post(
            '/auth/signin',
            data={
                'username': admin_user_info['email'],
                'password': 'WrongPassword123!',
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Invalid credentials'}

    async def test_non_existing_user_should_return_not_found_error(
        self, client: AsyncClient, admin_user_info: dict
    ):
        response = await client.post(
            '/auth/signin',
            data={
                'username': admin_user_info['email'],
                'password': admin_user_info['password'],
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Not found'}
