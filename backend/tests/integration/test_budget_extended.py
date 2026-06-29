"""
Unit tests for Budget module
Tests validation, error handling, and edge cases
"""
import pytest
from fastapi.testclient import TestClient
from main import app
import allure


@allure.parent_suite("Backend API")
@allure.suite("Budget")
@allure.feature("Budget Management")
@allure.story("Create Budget")
class TestCreateBudget:
    """Test budget creation functionality"""

    @allure.title("Successful budget creation")
    @allure.description("Verify that a budget can be created with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_budget_success(self, test_client, auth_headers):
        response = test_client.post("/api/budget", json={
            "category": "Food",
            "limit": 1000
        }, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["category"] == "Food"
        assert response.json()["limit"] == 1000

    @allure.title("Budget creation with missing category")
    @allure.description("Verify that budget creation fails when category is missing")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_budget_missing_category(self, test_client, auth_headers):
        response = test_client.post("/api/budget", json={
            "limit": 1000
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Budget creation with missing limit")
    @allure.description("Verify that budget creation fails when limit is missing")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_budget_missing_limit(self, test_client, auth_headers):
        response = test_client.post("/api/budget", json={
            "category": "Food"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Budget creation with negative limit")
    @allure.description("Verify that budget creation fails with negative limit")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_budget_negative_limit(self, test_client, auth_headers):
        response = test_client.post("/api/budget", json={
            "category": "Food",
            "limit": -100
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Budget creation with zero limit")
    @allure.description("Verify that budget creation fails with zero limit")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_budget_zero_limit(self, test_client, auth_headers):
        response = test_client.post("/api/budget", json={
            "category": "Food",
            "limit": 0
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Budget creation without authentication")
    @allure.description("Verify that budget creation fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_budget_unauthorized(self, test_client):
        response = test_client.post("/api/budget", json={
            "category": "Food",
            "limit": 1000
        })
        
        assert response.status_code == 401

    @allure.title("Budget creation with empty category")
    @allure.description("Verify that budget creation fails with empty category")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_budget_empty_category(self, test_client, auth_headers):
        response = test_client.post("/api/budget", json={
            "category": "",
            "limit": 1000
        }, headers=auth_headers)
        
        assert response.status_code == 422


@allure.parent_suite("Backend API")
@allure.suite("Budget")
@allure.feature("Budget Management")
@allure.story("Get Budgets")
class TestGetBudgets:
    """Test budget retrieval functionality"""

    @allure.title("Get all budgets successfully")
    @allure.description("Verify that all budgets can be retrieved for authenticated user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_budgets_success(self, test_client, auth_headers):
        # Create a budget first
        test_client.post("/api/budget", json={
            "category": "Food",
            "limit": 1000
        }, headers=auth_headers)
        
        response = test_client.get("/api/budget", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

    @allure.title("Get budgets without authentication")
    @allure.description("Verify that budget retrieval fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_budgets_unauthorized(self, test_client):
        response = test_client.get("/api/budget")
        
        assert response.status_code == 401

    @allure.title("Get budgets returns empty list for new user")
    @allure.description("Verify that new user gets empty budget list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_budgets_empty(self, test_client, auth_headers):
        response = test_client.get("/api/budget", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0


@allure.parent_suite("Backend API")
@allure.suite("Budget")
@allure.feature("Budget Management")
@allure.story("Update Budget")
class TestUpdateBudget:
    """Test budget update functionality"""

    @allure.title("Update budget successfully")
    @allure.description("Verify that a budget can be updated with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_budget_success(self, test_client, auth_headers):
        # Create a budget first
        create_response = test_client.post("/api/budget", json={
            "category": "Food",
            "limit": 1000
        }, headers=auth_headers)
        
        budget_id = create_response.json()["id"]
        
        # Update the budget
        response = test_client.put(f"/api/budget/{budget_id}", json={
            "category": "Food",
            "limit": 1500
        }, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["limit"] == 1500

    @allure.title("Update budget with invalid ID")
    @allure.description("Verify that budget update fails with non-existent ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_budget_invalid_id(self, test_client, auth_headers):
        response = test_client.put("/api/budget/99999", json={
            "category": "Food",
            "limit": 1500
        }, headers=auth_headers)
        
        assert response.status_code == 404

    @allure.title("Update budget without authentication")
    @allure.description("Verify that budget update fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_budget_unauthorized(self, test_client):
        response = test_client.put("/api/budget/1", json={
            "category": "Food",
            "limit": 1500
        })
        
        assert response.status_code == 401


@allure.parent_suite("Backend API")
@allure.suite("Budget")
@allure.feature("Budget Management")
@allure.story("Delete Budget")
class TestDeleteBudget:
    """Test budget deletion functionality"""

    @allure.title("Delete budget successfully")
    @allure.description("Verify that a budget can be deleted")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_budget_success(self, test_client, auth_headers):
        # Create a budget first
        create_response = test_client.post("/api/budget", json={
            "category": "Food",
            "limit": 1000
        }, headers=auth_headers)
        
        budget_id = create_response.json()["id"]
        
        # Delete the budget
        response = test_client.delete(f"/api/budget/{budget_id}", headers=auth_headers)
        
        assert response.status_code == 200

    @allure.title("Delete budget with invalid ID")
    @allure.description("Verify that budget deletion fails with non-existent ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_budget_invalid_id(self, test_client, auth_headers):
        response = test_client.delete("/api/budget/99999", headers=auth_headers)
        
        assert response.status_code == 404

    @allure.title("Delete budget without authentication")
    @allure.description("Verify that budget deletion fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_budget_unauthorized(self, test_client):
        response = test_client.delete("/api/budget/1")
        
        assert response.status_code == 401
