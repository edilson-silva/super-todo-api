from fastapi import status
from httpx import Client


class TestApp:
    def test_root_endpoint_should_redirect_to_docs_endpoint(
        self, client_with_mock_deps: Client
    ):
        response = client_with_mock_deps.get('/', follow_redirects=False)

        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers['location'] == '/docs'

        response = client_with_mock_deps.get('/docs')

        assert response.status_code == status.HTTP_200_OK
        assert 'SuperTodo - Swagger UI' in response.text

    def test_api_v1_endpoint_should_redirect_to_docs_endpoint(
        self, client_with_mock_deps: Client
    ):
        response = client_with_mock_deps.get('/api/v1', follow_redirects=False)

        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers['location'] == 'http://testserver/api/v1/'

        response = client_with_mock_deps.get('/api/v1')

        assert response.status_code == status.HTTP_200_OK
        assert 'SuperTodo - Swagger UI' in response.text

    def test_docs_enpoint_should_return_doc(
        self, client_with_mock_deps: Client
    ):
        response = client_with_mock_deps.get('/docs')

        assert response.status_code == status.HTTP_200_OK
        assert 'SuperTodo - Swagger UI' in response.text
