import pytest
import allure


@allure.parent_suite("Backend API")
@allure.suite("Expense")
@allure.feature("Expense Management")
@allure.story("Create Expense")
class TestCreateExpense:
    """Integration tests for expense creation"""

    @allure.title("Integration test - Create expense")
    @allure.description("Verify expense creation through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_create_expense(self, test_client, auth_headers):
        res = test_client.post("/api/expense", json={
            "description": "Food",
            "amount": 200,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)

        assert res.status_code == 200
        assert res.json()["description"] == "Food"


@allure.parent_suite("Backend API")
@allure.suite("Expense")
@allure.feature("Expense Management")
@allure.story("Get Expenses")
class TestGetExpenses:
    """Integration tests for expense retrieval"""

    @allure.title("Integration test - Get expenses")
    @allure.description("Verify expense retrieval through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_get_expenses(self, test_client, auth_headers):
        res = test_client.get("/api/expense", headers=auth_headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)
