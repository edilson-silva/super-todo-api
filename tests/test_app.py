from fastapi import status
from fastapi.testclient import TestClient

from src.main import app


def test_root_should_return_200():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert 'SuperTodo - Swagger UI' in response.text
