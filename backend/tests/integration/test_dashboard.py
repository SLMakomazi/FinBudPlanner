import pytest
import allure


@allure.parent_suite("Backend API")
@allure.suite("Dashboard")
@allure.feature("Dashboard")
@allure.story("Dashboard Summary")
class TestDashboardSummary:
    """Integration tests for dashboard summary"""

    @allure.title("Integration test - Dashboard summary")
    @allure.description("Verify dashboard summary through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_dashboard_summary(self, test_client, auth_headers):
        res = test_client.get("/api/dashboard/summary", headers=auth_headers)
        assert res.status_code == 200

        data = res.json()
        assert "total_income" in data
        assert "total_expenses" in data
        assert "net_balance" in data
        assert "savings_rate" in data


@allure.parent_suite("Backend API")
@allure.suite("Dashboard")
@allure.feature("Dashboard")
@allure.story("Recent Transactions")
class TestRecentTransactions:
    """Integration tests for recent transactions"""

    @allure.title("Integration test - Recent transactions")
    @allure.description("Verify recent transactions through API endpoint")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.integration
    def test_recent_transactions(self, test_client, auth_headers):
        res = test_client.get("/api/dashboard/recent-transactions", headers=auth_headers)
        assert res.status_code == 200
        assert isinstance(res.json(), list)
