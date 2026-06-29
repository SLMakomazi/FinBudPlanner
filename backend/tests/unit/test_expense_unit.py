"""
Unit tests for Expense module
Tests validation, error handling, and edge cases
"""
import pytest
from fastapi.testclient import TestClient
from main import app
import allure


@allure.parent_suite("Backend API")
@allure.suite("Expense")
@allure.feature("Expense Management")
@allure.story("Create Expense")
class TestCreateExpense:
    """Test expense creation functionality"""

    @allure.title("Successful expense creation")
    @allure.description("Verify that an expense can be created with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_expense_success(self, test_client, auth_headers):
        response = test_client.post("/api/expense", json={
            "description": "Food",
            "amount": 200,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["description"] == "Food"
        assert response.json()["amount"] == 200

    @allure.title("Expense creation with missing description")
    @allure.description("Verify that expense creation fails when description is missing")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_expense_missing_description(self, test_client, auth_headers):
        response = test_client.post("/api/expense", json={
            "amount": 200,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Expense creation with missing amount")
    @allure.description("Verify that expense creation fails when amount is missing")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_expense_missing_amount(self, test_client, auth_headers):
        response = test_client.post("/api/expense", json={
            "description": "Food",
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Expense creation with negative amount")
    @allure.description("Verify that expense creation fails with negative amount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_expense_negative_amount(self, test_client, auth_headers):
        response = test_client.post("/api/expense", json={
            "description": "Food",
            "amount": -100,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Expense creation with zero amount")
    @allure.description("Verify that expense creation fails with zero amount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_expense_zero_amount(self, test_client, auth_headers):
        response = test_client.post("/api/expense", json={
            "description": "Food",
            "amount": 0,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Expense creation with invalid date format")
    @allure.description("Verify that expense creation fails with invalid date format")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_expense_invalid_date(self, test_client, auth_headers):
        response = test_client.post("/api/expense", json={
            "description": "Food",
            "amount": 200,
            "date": "invalid-date",
            "category": "Daily"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Expense creation without authentication")
    @allure.description("Verify that expense creation fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_expense_unauthorized(self, test_client):
        response = test_client.post("/api/expense", json={
            "description": "Food",
            "amount": 200,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        })
        
        assert response.status_code == 401


@allure.parent_suite("Backend API")
@allure.suite("Expense")
@allure.feature("Expense Management")
@allure.story("Get Expenses")
class TestGetExpenses:
    """Test expense retrieval functionality"""

    @allure.title("Get all expenses successfully")
    @allure.description("Verify that all expense records can be retrieved for authenticated user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_expenses_success(self, test_client, auth_headers):
        # Create an expense first
        test_client.post("/api/expense", json={
            "description": "Food",
            "amount": 200,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        response = test_client.get("/api/expense", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

    @allure.title("Get expenses without authentication")
    @allure.description("Verify that expense retrieval fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_expenses_unauthorized(self, test_client):
        response = test_client.get("/api/expense")
        
        assert response.status_code == 401

    @allure.title("Get expenses returns empty list for new user")
    @allure.description("Verify that new user gets empty expense list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_expenses_empty(self, test_client, auth_headers):
        response = test_client.get("/api/expense", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0


@allure.parent_suite("Backend API")
@allure.suite("Expense")
@allure.feature("Expense Management")
@allure.story("Update Expense")
class TestUpdateExpense:
    """Test expense update functionality"""

    @allure.title("Update expense successfully")
    @allure.description("Verify that an expense can be updated with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_expense_success(self, test_client, auth_headers):
        # Create an expense first
        create_response = test_client.post("/api/expense", json={
            "description": "Food",
            "amount": 200,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        expense_id = create_response.json()["id"]
        
        # Update the expense
        response = test_client.put(f"/api/expense/{expense_id}", json={
            "description": "Groceries",
            "amount": 300,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["description"] == "Groceries"
        assert response.json()["amount"] == 300

    @allure.title("Update expense with invalid ID")
    @allure.description("Verify that expense update fails with non-existent ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_expense_invalid_id(self, test_client, auth_headers):
        response = test_client.put("/api/expense/99999", json={
            "description": "Groceries",
            "amount": 300,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        assert response.status_code == 404

    @allure.title("Update expense without authentication")
    @allure.description("Verify that expense update fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_expense_unauthorized(self, test_client):
        response = test_client.put("/api/expense/1", json={
            "description": "Groceries",
            "amount": 300,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        })
        
        assert response.status_code == 401


@allure.parent_suite("Backend API")
@allure.suite("Expense")
@allure.feature("Expense Management")
@allure.story("Delete Expense")
class TestDeleteExpense:
    """Test expense deletion functionality"""

    @allure.title("Delete expense successfully")
    @allure.description("Verify that an expense can be deleted")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_expense_success(self, test_client, auth_headers):
        # Create an expense first
        create_response = test_client.post("/api/expense", json={
            "description": "Food",
            "amount": 200,
            "date": "2026-01-01T00:00:00",
            "category": "Daily"
        }, headers=auth_headers)
        
        expense_id = create_response.json()["id"]
        
        # Delete the expense
        response = test_client.delete(f"/api/expense/{expense_id}", headers=auth_headers)
        
        assert response.status_code == 200

    @allure.title("Delete expense with invalid ID")
    @allure.description("Verify that expense deletion fails with non-existent ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_expense_invalid_id(self, test_client, auth_headers):
        response = test_client.delete("/api/expense/99999", headers=auth_headers)
        
        assert response.status_code == 404

    @allure.title("Delete expense without authentication")
    @allure.description("Verify that expense deletion fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_expense_unauthorized(self, test_client):
        response = test_client.delete("/api/expense/1")
        
        assert response.status_code == 401
