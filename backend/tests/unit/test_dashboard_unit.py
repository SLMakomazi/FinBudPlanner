"""
Unit tests for Dashboard module
Tests validation, error handling, and edge cases
"""
import pytest
from fastapi.testclient import TestClient
from main import app
import allure


@allure.parent_suite("Backend API")
@allure.suite("Dashboard")
@allure.feature("Dashboard")
@allure.story("Dashboard Summary")
class TestDashboardSummary:
    """Test dashboard summary functionality"""

    @allure.title("Get dashboard summary successfully")
    @allure.description("Verify that dashboard summary returns correct data structure")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_dashboard_summary_success(self, test_client, auth_headers):
        response = test_client.get("/api/dashboard/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_income" in data
        assert "total_expenses" in data
        assert "net_balance" in data
        assert "savings_rate" in data

    @allure.title("Get dashboard summary without authentication")
    @allure.description("Verify that dashboard summary fails without authentication")
    @allure.severity(allure.severity_level.HIGH)
    def test_dashboard_summary_unauthorized(self, test_client):
        response = test_client.get("/api/dashboard/summary")
        
        assert response.status_code == 401

    @allure.title("Dashboard summary returns numeric values")
    @allure.description("Verify that dashboard summary returns numeric financial values")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_dashboard_summary_numeric_values(self, test_client, auth_headers):
        response = test_client.get("/api/dashboard/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["total_income"], (int, float))
        assert isinstance(data["total_expenses"], (int, float))
        assert isinstance(data["net_balance"], (int, float))
        assert isinstance(data["savings_rate"], (int, float))


@allure.parent_suite("Backend API")
@allure.suite("Dashboard")
@allure.feature("Dashboard")
@allure.story("Recent Transactions")
class TestRecentTransactions:
    """Test recent transactions functionality"""

    @allure.title("Get recent transactions successfully")
    @allure.description("Verify that recent transactions can be retrieved")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_recent_transactions_success(self, test_client, auth_headers):
        response = test_client.get("/api/dashboard/recent-transactions", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @allure.title("Get recent transactions without authentication")
    @allure.description("Verify that recent transactions fails without authentication")
    @allure.severity(allure.severity_level.HIGH)
    def test_recent_transactions_unauthorized(self, test_client):
        response = test_client.get("/api/dashboard/recent-transactions")
        
        assert response.status_code == 401

    @allure.title("Recent transactions returns empty list for new user")
    @allure.description("Verify that new user gets empty recent transactions list")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_recent_transactions_empty(self, test_client, auth_headers):
        response = test_client.get("/api/dashboard/recent-transactions", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0

    @allure.title("Recent transactions with income and expense")
    @allure.description("Verify that recent transactions includes both income and expenses")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_recent_transactions_with_data(self, test_client, auth_headers):
        # Create income
        test_client.post("/api/income", json={
            "source": "Salary",
            "amount": 5000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        # Create expense
        test_client.post("/api/expense", json={
            "description": "Food",
            "amount": 200,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        response = test_client.get("/api/dashboard/recent-transactions", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 2
