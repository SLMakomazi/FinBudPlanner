import pytest
import allure


@allure.parent_suite("Backend API")
@allure.suite("Users")
@allure.feature("User Management")
@allure.story("Get Current User")
class TestGetCurrentUser:
    """Integration tests for current user retrieval"""

    @allure.title("Integration test - Get current user")
    @allure.description("Verify current user retrieval through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_get_me(self, test_client, auth_headers):
        res = test_client.get("/api/users/me", headers=auth_headers)
        assert res.status_code == 200
        assert "username" in res.json()
