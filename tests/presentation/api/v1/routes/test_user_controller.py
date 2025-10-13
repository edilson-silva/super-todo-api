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
CreateUserSetupType = Tuple[AsyncClient, dict, dict, dict]


@pytest.fixture
def setup(
    admin_company_users: UsersList,
    admin_user_token: TokenGeneratorEncodeOutputDTO,
    basic_user: User,
    basic_user_token: TokenGeneratorEncodeOutputDTO,
    client: AsyncClient,
) -> SetupType:
    users = UsersList
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


@pytest.fixture
def create_user_setup(setup: SetupType) -> CreateUserSetupType:
    client, admin_user_headers, basic_user_headers, new_user_sample, _ = setup

    return (
        client,
        admin_user_headers,
        basic_user_headers,
        new_user_sample,
    )


@pytest.mark.asyncio
class TestUserCreateController:
    async def test_missing_request_params_should_return_unprocessable_error(
        self, create_user_setup: CreateUserSetupType
    ):
        client, admin_user_headers, _, _ = create_user_setup

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
        self, create_user_setup: CreateUserSetupType, datetime_to_web_iso
    ):
        client, admin_user_headers, basic_user_headers, new_user_sample = (
            create_user_setup
        )

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
        self, create_user_setup: CreateUserSetupType, datetime_to_web_iso
    ):
        client, admin_user_headers, basic_user_headers, new_user_sample = (
            create_user_setup
        )

        response1 = await client.post(
            '/users', headers=admin_user_headers, json=new_user_sample
        )

        assert response1.status_code == status.HTTP_201_CREATED

        response2 = await client.post(
            '/users', headers=admin_user_headers, json=new_user_sample
        )

        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert response2.json() == {'detail': 'Bad Request'}
