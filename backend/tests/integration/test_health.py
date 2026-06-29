"""Backend health-check integration tests for CI."""
import pytest
import allure


@allure.parent_suite("Backend API")
@allure.suite("Health")
@allure.feature("Health Check")
@allure.story("Health Endpoint")
class TestHealthEndpoint:
    """Integration tests for health check endpoint"""

    @allure.title("Integration test - Health check")
    @allure.description("Verify health check endpoint returns healthy status")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_health_check_returns_healthy_status(self, test_client):
        response = test_client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}