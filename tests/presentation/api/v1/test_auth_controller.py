from fastapi import status
from httpx import Client


class TestAuthController:
    new_user_info = {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': '123456789',
    }

    def test_signup_with_invalid_request_params_should_return_error(
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

    def test_signup_with_new_user_info_should_return_success(
        self, client_with_mock_deps: Client
    ):
        response = client_with_mock_deps.post(
            '/auth/signup', json=TestAuthController.new_user_info
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.text == 'null'
