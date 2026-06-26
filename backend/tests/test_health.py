"""Backend health-check unit tests for CI."""

def test_health_check_returns_healthy_status(test_client):
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}