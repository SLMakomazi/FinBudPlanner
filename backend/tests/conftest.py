import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def client():
    return client


@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "password": "TestPass123!"
    }


@pytest.fixture
def auth_headers(client, test_user):
    client.post("/api/register", json=test_user)

    response = client.post(
        "/api/token",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }