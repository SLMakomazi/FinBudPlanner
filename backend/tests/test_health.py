"""Backend health-check unit tests for CI."""

import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_check_returns_healthy_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
