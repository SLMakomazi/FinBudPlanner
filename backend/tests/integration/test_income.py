import pytest
import allure


@allure.parent_suite("Backend API")
@allure.suite("Income")
@allure.feature("Income Management")
@allure.story("Create Income")
class TestCreateIncome:
    """Integration tests for income creation"""

    @allure.title("Integration test - Create income")
    @allure.description("Verify income creation through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_create_income(self, test_client, auth_headers):
        res = test_client.post("/api/income", json={
            "source": "Salary",
            "amount": 5000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)

        assert res.status_code == 200
        assert res.json()["source"] == "Salary"


@allure.parent_suite("Backend API")
@allure.suite("Income")
@allure.feature("Income Management")
@allure.story("Get Income")
class TestGetIncome:
    """Integration tests for income retrieval"""

    @allure.title("Integration test - Get income")
    @allure.description("Verify income retrieval through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_get_income(self, test_client, auth_headers):
        res = test_client.get("/api/income", headers=auth_headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)
