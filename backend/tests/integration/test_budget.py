import pytest
import allure


@allure.parent_suite("Backend API")
@allure.suite("Budget")
@allure.feature("Budget Management")
@allure.story("Create Budget")
class TestCreateBudget:
    """Integration tests for budget creation"""

    @allure.title("Integration test - Create budget")
    @allure.description("Verify budget creation through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_create_budget(self, test_client, auth_headers):
        res = test_client.post("/api/budget", json={
            "category": "Food",
            "limit": 1000
        }, headers=auth_headers)

        assert res.status_code == 200
        assert res.json()["category"] == "Food"


@allure.parent_suite("Backend API")
@allure.suite("Budget")
@allure.feature("Budget Management")
@allure.story("Get Budgets")
class TestGetBudgets:
    """Integration tests for budget retrieval"""

    @allure.title("Integration test - Get budgets")
    @allure.description("Verify budget retrieval through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_get_budgets(self, test_client, auth_headers):
        res = test_client.get("/api/budget", headers=auth_headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)
