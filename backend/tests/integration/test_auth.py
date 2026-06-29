import pytest
import allure


@allure.parent_suite("Backend API")
@allure.suite("Authentication")
@allure.feature("Authentication")
@allure.story("User Registration")
class TestUserRegistration:
    """Integration tests for user registration"""

    @allure.title("Integration test - User registration")
    @allure.description("Verify user registration through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_register(self, test_client):
        res = test_client.post("/api/register", json={
            "username": "user1",
            "password": "Password123!"
        })
        assert res.status_code == 200
        assert "id" in res.json()


@allure.parent_suite("Backend API")
@allure.suite("Authentication")
@allure.feature("Authentication")
@allure.story("User Login")
class TestUserLogin:
    """Integration tests for user login"""

    @allure.title("Integration test - User login")
    @allure.description("Verify user login through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_login(self, test_client):
        test_client.post("/api/register", json={
            "username": "user2",
            "password": "Password123!"
        })

        res = test_client.post("/api/token", data={
            "username": "user2",
            "password": "Password123!"
        })

        assert res.status_code == 200
        assert "access_token" in res.json()
