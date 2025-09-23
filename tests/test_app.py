from fastapi import status
from httpx import AsyncClient


class TestApp:
    async def test_root_endpoint_should_redirect_to_docs_endpoint(
        self, client: AsyncClient
    ):
        response = await client.get('/', follow_redirects=False)

        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers['location'] == '/docs'

        response = await client.get('/docs')

        assert response.status_code == status.HTTP_200_OK
        assert 'SuperTodo - Swagger UI' in response.text

    async def test_api_v1_endpoint_should_redirect_to_docs_endpoint(
        self, client: AsyncClient
    ):
        response = await client.get('/api/v1', follow_redirects=False)

        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers['location'] == 'http://test/api/v1/'

        response = await client.get('/api/v1')

        assert response.status_code == status.HTTP_200_OK
        assert 'SuperTodo - Swagger UI' in response.text

    async def test_docs_enpoint_should_return_doc(self, client: AsyncClient):
        response = await client.get('/docs')

        assert response.status_code == status.HTTP_200_OK
        assert 'SuperTodo - Swagger UI' in response.text
