from fastapi import status
from httpx import Client


class AppTest:
    def test_root_enpoint_should_return_doc(
        self, client_with_mock_deps: Client
    ):
        response = client_with_mock_deps.get('/')

        assert response.status_code == status.HTTP_200_OK
        assert 'SuperTodo - Swagger UI' in response.text

    def test_api_v1_enpoint_should_return_doc(
        self, client_with_mock_deps: Client
    ):
        response = client_with_mock_deps.get('/api/v1')

        assert response.status_code == status.HTTP_200_OK
        assert 'SuperTodo - Swagger UI' in response.text

    def test_docs_enpoint_should_return_doc(
        self, client_with_mock_deps: Client
    ):
        response = client_with_mock_deps.get('/api/v1')

        assert response.status_code == status.HTTP_200_OK
        assert 'SuperTodo - Swagger UI' in response.text
