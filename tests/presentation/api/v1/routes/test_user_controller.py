from datetime import datetime, timezone
from typing import List, Tuple

import pytest
from fastapi import status
from freezegun import freeze_time
from httpx import AsyncClient

from src.application.dtos.security.token_generator_encode_dto import (
    TokenGeneratorEncodeOutputDTO,
)
from src.domain.entities.user_entity import User

mock_create_datetime = datetime(
    2025,
    1,
    1,
    0,
    0,
    0,
    0,
    timezone.utc,
)
mock_update_datetime = datetime(
    2025,
    1,
    1,
    0,
    5,
    0,
    0,
    timezone.utc,
)

UsersList = List[User]
SetupType = Tuple[AsyncClient, dict, dict, dict, UsersList]
UserCreateSetupType = Tuple[AsyncClient, dict, dict, dict]
UserListSetupType = SetupType
UserGetSetupType = Tuple[AsyncClient, dict, UsersList]


@pytest.fixture
def setup(
    admin_company_users: UsersList,
    admin_user_token: TokenGeneratorEncodeOutputDTO,
    basic_user: User,
    basic_user_token: TokenGeneratorEncodeOutputDTO,
    client: AsyncClient,
) -> SetupType:
    users = admin_company_users
    admin_user_access_token = (
        f'{admin_user_token.token_type} {admin_user_token.access_token}'
    )
    admin_user_headers = {'Authorization': admin_user_access_token}
    basic_user_access_token = (
        f'{basic_user_token.token_type} {basic_user_token.access_token}'
    )
    basic_user_headers = {'Authorization': basic_user_access_token}
    new_user_sample = {
        'name': 'sample',
        'email': 'sample@mail.com',
        'password': '123456789',
        'role': 'admin',
        'avatar': '',
    }
    return (
        client,
        admin_user_headers,
        basic_user_headers,
        new_user_sample,
        users,
    )


@pytest.mark.asyncio
class TestUserCreateController:
    @pytest.fixture
    def user_create_setup(self, setup: SetupType) -> UserCreateSetupType:
        client, admin_user_headers, basic_user_headers, new_user_sample, _ = (
            setup
        )

        return (
            client,
            admin_user_headers,
            basic_user_headers,
            new_user_sample,
        )

    async def test_missing_token_should_return_unauthorized_error(
        self, user_create_setup: UserCreateSetupType
    ):
        client, admin_user_headers, _, _ = user_create_setup

        response = await client.post('/users')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Not authenticated'}

    async def test_non_admin_requester_should_return_forbidden_error(
        self, user_create_setup: UserCreateSetupType
    ):
        client, _, basic_user_headers, new_user_sample = user_create_setup

        response = await client.post(
            '/users', headers=basic_user_headers, json=new_user_sample
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Unauthorized'}

    async def test_missing_request_params_should_return_unprocessable_error(
        self, user_create_setup: UserCreateSetupType
    ):
        client, admin_user_headers, _, _ = user_create_setup

        response = await client.post(
            '/users', headers=admin_user_headers, json={}
        )

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

    @freeze_time(mock_create_datetime.isoformat())
    async def test_create_user_info_should_return_success(
        self, user_create_setup: UserCreateSetupType, datetime_to_web_iso
    ):
        client, admin_user_headers, _, new_user_sample = user_create_setup

        response = await client.post(
            '/users', headers=admin_user_headers, json=new_user_sample
        )

        assert response.status_code == status.HTTP_201_CREATED

        created_user = response.json()

        assert isinstance(created_user['id'], str)
        assert created_user['id'] != ''
        assert created_user['name'] == new_user_sample['name']
        assert created_user['email'] == new_user_sample['email']
        assert created_user['role'] == new_user_sample['role']
        assert created_user['avatar'] == new_user_sample['avatar']
        assert created_user['created_at'] == datetime_to_web_iso(
            mock_create_datetime
        )
        assert created_user['updated_at'] == datetime_to_web_iso(
            mock_create_datetime
        )

    async def test_existing_user_info_should_return_bad_request_error(
        self, user_create_setup: UserCreateSetupType, datetime_to_web_iso
    ):
        client, admin_user_headers, _, new_user_sample = user_create_setup

        response1 = await client.post(
            '/users', headers=admin_user_headers, json=new_user_sample
        )

        assert response1.status_code == status.HTTP_201_CREATED

        response2 = await client.post(
            '/users', headers=admin_user_headers, json=new_user_sample
        )

        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert response2.json() == {'detail': 'Bad Request'}


@pytest.mark.asyncio
class TestUserListController:
    @pytest.fixture
    def user_list_setup(self, setup: SetupType) -> UserListSetupType:
        return setup

    async def test_missing_token_should_return_unauthorized_error(
        self, user_list_setup: UserListSetupType
    ):
        client, admin_user_headers, _, _, _ = user_list_setup

        response = await client.get('/users')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Not authenticated'}

    async def test_non_admin_requester_should_return_forbidden_error(
        self, user_list_setup: UserListSetupType
    ):
        client, _, basic_user_headers, _, _ = user_list_setup

        response = await client.get('/users', headers=basic_user_headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Unauthorized'}

    async def test_should_return_a_list_with_six_users(
        self, user_list_setup: UserListSetupType, datetime_to_web_iso
    ):
        client, admin_user_headers, _, _, users = user_list_setup

        response = await client.get('/users', headers=admin_user_headers)

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert 'data' in response_data

        users_expected = response_data['data']

        assert isinstance(users_expected, list)
        assert len(users_expected) == 6

        for user, user_expected in zip(users, users_expected):
            assert user.name == user_expected['name']
            assert user.id == user_expected['id']
            assert user.name == user_expected['name']
            assert user.email == user_expected['email']
            assert user.role == user_expected['role']
            assert (
                datetime_to_web_iso(user.created_at)
                == user_expected['created_at']
            )
            assert (
                datetime_to_web_iso(user.updated_at)
                == user_expected['updated_at']
            )

    async def test_should_use_limit_param_and_return_a_list_with_two_users(
        self, user_list_setup: UserListSetupType, datetime_to_web_iso
    ):
        client, admin_user_headers, _, _, users = user_list_setup

        response = await client.get(
            '/users?limit=2&skip=0', headers=admin_user_headers
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert 'data' in response_data

        users_expected = response_data['data']

        assert isinstance(users_expected, list)
        assert len(users_expected) == 2

        for user, user_expected in zip(users, users_expected):
            assert user.name == user_expected['name']
            assert user.id == user_expected['id']
            assert user.name == user_expected['name']
            assert user.email == user_expected['email']
            assert user.role == user_expected['role']
            assert (
                datetime_to_web_iso(user.created_at)
                == user_expected['created_at']
            )
            assert (
                datetime_to_web_iso(user.updated_at)
                == user_expected['updated_at']
            )

    async def test_should_use_offset_param_and_return_a_list_with_two_users(
        self, user_list_setup: UserListSetupType, datetime_to_web_iso
    ):
        client, admin_user_headers, _, _, users = user_list_setup

        response = await client.get(
            '/users?limit=2&offset=2', headers=admin_user_headers
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert 'data' in response_data

        users_expected = response_data['data']

        assert isinstance(users_expected, list)
        assert len(users_expected) == 2

        for user, user_expected in zip(users[2:4], users_expected[2:4]):
            assert user.name == user_expected['name']
            assert user.id == user_expected['id']
            assert user.name == user_expected['name']
            assert user.email == user_expected['email']
            assert user.role == user_expected['role']
            assert (
                datetime_to_web_iso(user.created_at)
                == user_expected['created_at']
            )
            assert (
                datetime_to_web_iso(user.updated_at)
                == user_expected['updated_at']
            )

    async def test_should_return_an_empty_list(
        self, user_list_setup: UserListSetupType
    ):
        client, admin_user_headers, _, _, _ = user_list_setup

        response = await client.get(
            '/users?offset=10', headers=admin_user_headers
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert 'data' in response_data

        users_expected = response_data['data']

        assert isinstance(users_expected, list)
        assert len(users_expected) == 0


@pytest.mark.asyncio
class TestUserGettController:
    @pytest.fixture
    def user_get_setup(self, setup: SetupType) -> UserGetSetupType:
        client, admin_user_headers, _, _, users = setup

        return (
            client,
            admin_user_headers,
            users,
        )

    async def test_missing_token_should_return_unauthorized_error(
        self, user_get_setup: UserGetSetupType
    ):
        client, _, users = user_get_setup

        response = await client.get(f'/users/{users[0].id}')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Not authenticated'}
