from datetime import datetime, timezone

import pytest
from fastapi import status
from freezegun import freeze_time
from httpx import AsyncClient

from src.domain.entities.user_role import UserRole

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


@pytest.mark.asyncio
class TestUserCreateController:
    async def test_missing_request_params_should_return_unprocessable_error(
        self, client: AsyncClient
    ):
        response = await client.post('/users', json={})

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

    @freeze_time(mock_datetime.isoformat())
    async def test_create_user_info_should_return_success(
        self,
        client: AsyncClient,
        sample_user_info: dict,
        datetime_to_web_iso,
    ):
        response = await client.post('/users', json=sample_user_info)

        assert response.status_code == status.HTTP_201_CREATED

        created_user = response.json()

        assert isinstance(created_user['id'], str)
        assert created_user['id'] != ''
        assert created_user['name'] == 'Test User'
        assert created_user['email'] == 'test@example.com'
        assert created_user['role'] == 'admin'
        assert created_user['avatar'] == ''
        assert created_user['created_at'] == datetime_to_web_iso(mock_datetime)

    async def test_existing_user_info_should_return_bad_request_error(
        self, client: AsyncClient, sample_user_info: dict
    ):
        response1 = await client.post('/users', json=sample_user_info)

        assert response1.status_code == status.HTTP_201_CREATED

        created_user = response1.json()

        assert isinstance(created_user['id'], str)
        assert created_user['id'] != ''
        assert created_user['name'] == 'Test User'
        assert created_user['email'] == 'test@example.com'
        assert created_user['role'] == 'admin'
        assert created_user['avatar'] == ''

        response2 = await client.post('/users', json=sample_user_info)

        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert response2.json() == {'detail': 'Bad Request'}


class TestUserGetController:
    @freeze_time(mock_datetime.isoformat())
    async def test_valid_id_should_return_success(
        self, client: AsyncClient, sample_user_info: dict, datetime_to_web_iso
    ):
        user_create_response = await client.post(
            '/users', json=sample_user_info
        )

        assert user_create_response.status_code == status.HTTP_201_CREATED

        user_created = user_create_response.json()

        user_get_response = await client.get(f'/users/{user_created["id"]}')

        assert user_get_response.status_code == status.HTTP_200_OK

        user_found = user_get_response.json()

        assert user_found['id'] == user_created['id']
        assert user_found['name'] == user_created['name']
        assert user_found['email'] == user_created['email']
        assert user_found['role'] == user_created['role']
        assert user_found['avatar'] == user_created['avatar']
        assert user_found['created_at'] == datetime_to_web_iso(mock_datetime)

    async def test_invalid_id_should_return_not_found_error(
        self, client: AsyncClient, sample_user_info: dict
    ):
        response = await client.get('/users/invalid-id')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Not Found'}


class TestUserListController:
    @freeze_time(mock_datetime.isoformat())
    async def test_should_return_success(
        self, client: AsyncClient, sample_user_info: dict, datetime_to_web_iso
    ):
        user_create_response = await client.post(
            '/users', json=sample_user_info
        )

        assert user_create_response.status_code == status.HTTP_201_CREATED

        user_created = user_create_response.json()

        user_list_response = await client.get('/users')

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
        assert user['created_at'] == datetime_to_web_iso(mock_datetime)


class TestUserDeleteController:
    async def test_valid_id_should_return_success(
        self, client: AsyncClient, sample_user_info: dict
    ):
        user_create_response = await client.post(
            '/users', json=sample_user_info
        )

        assert user_create_response.status_code == status.HTTP_201_CREATED

        user_created = user_create_response.json()

        user_delete_response = await client.delete(
            f'/users/{user_created["id"]}'
        )

        assert user_delete_response.status_code == status.HTTP_204_NO_CONTENT

    async def test_invalid_id_should_return_not_found_error(
        self, client: AsyncClient, sample_user_info: dict
    ):
        response = await client.delete('/users/invalid-id')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Not Found'}


class TestUserUpdateController:
    async def test_missing_request_params_should_return_unprocessable_error(
        self, client: AsyncClient
    ):
        response = await client.put('/users/random-id', json={})

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
                    'loc': ['body', 'password'],
                    'msg': 'Field required',
                    'input': {},
                },
                {
                    'type': 'missing',
                    'loc': ['body', 'role'],
                    'msg': 'Field required',
                    'input': {},
                },
                {
                    'type': 'missing',
                    'loc': ['body', 'avatar'],
                    'msg': 'Field required',
                    'input': {},
                },
            ]
        }

    async def test_valid_id_should_return_success(
        self, client: AsyncClient, sample_user_info: dict
    ):
        user_create_response = await client.post(
            '/users', json=sample_user_info
        )

        assert user_create_response.status_code == status.HTTP_201_CREATED

        user_created = user_create_response.json()

        user_update_info = {
            'name': 'Updated Name',
            'password': 'updated_pass',
            'role': UserRole.USER,
            'avatar': 'updated_avatar',
        }

        user_update_response = await client.put(
            f'/users/{user_created["id"]}', json=user_update_info
        )

        assert user_update_response.status_code == status.HTTP_200_OK

        user_updated = user_update_response.json()

        assert user_updated['id'] == user_created['id']
        assert user_updated['name'] == user_update_info['name']
        assert user_updated['email'] == user_created['email']
        assert user_updated['avatar'] == user_update_info['avatar']
        assert user_updated['role'] == user_update_info['role']
        assert user_updated['created_at'] == user_created['created_at']

    async def test_invalid_id_should_return_not_found_error(
        self, client: AsyncClient, sample_user_info: dict
    ):
        response = await client.put(
            '/users/invalid-id',
            json={
                'name': 'Updated Name',
                'password': 'updated_pass',
                'role': UserRole.USER,
                'avatar': 'updated_avatar',
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Not Found'}


class TestUserUpdatePartialController:
    async def test_valid_id_and_empty_request_params_should_return_success(
        self, client: AsyncClient, sample_user_info: dict
    ):
        user_create_response = await client.post(
            '/users', json=sample_user_info
        )

        assert user_create_response.status_code == status.HTTP_201_CREATED

        user_created = user_create_response.json()

        user_update_partial_info = {}

        user_update_response = await client.patch(
            f'/users/{user_created["id"]}', json=user_update_partial_info
        )

        assert user_update_response.status_code == status.HTTP_200_OK

        user_updated = user_update_response.json()

        assert user_updated['id'] == user_created['id']
        assert user_updated['name'] == user_created['name']
        assert user_updated['email'] == user_created['email']
        assert user_updated['avatar'] == user_created['avatar']
        assert user_updated['role'] == user_created['role']
        assert user_updated['created_at'] == user_created['created_at']

    async def test_valid_id_and_request_params_should_return_success(
        self, client: AsyncClient, sample_user_info: dict
    ):
        user_create_response = await client.post(
            '/users', json=sample_user_info
        )

        assert user_create_response.status_code == status.HTTP_201_CREATED

        user_created = user_create_response.json()

        user_update_partial_info = {
            'name': 'Updated Name',
            'password': 'updated_pass',
            'role': UserRole.USER,
            'avatar': 'updated_avatar',
        }

        user_update_response = await client.put(
            f'/users/{user_created["id"]}', json=user_update_partial_info
        )

        assert user_update_response.status_code == status.HTTP_200_OK

        user_updated = user_update_response.json()

        assert user_updated['id'] == user_created['id']
        assert user_updated['name'] == user_update_partial_info['name']
        assert user_updated['email'] == user_created['email']
        assert user_updated['avatar'] == user_update_partial_info['avatar']
        assert user_updated['role'] == user_update_partial_info['role']
        assert user_updated['created_at'] == user_created['created_at']

    async def test_invalid_id_should_return_not_found_error(
        self, client: AsyncClient, sample_user_info: dict
    ):
        response = await client.patch(
            '/users/invalid-id',
            json={},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {'detail': 'Not Found'}
