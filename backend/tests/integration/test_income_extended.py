"""
Unit tests for Income module
Tests validation, error handling, and edge cases
"""
import pytest
from fastapi.testclient import TestClient
from main import app
import allure


@allure.parent_suite("Backend API")
@allure.suite("Income")
@allure.feature("Income Management")
@allure.story("Create Income")
class TestCreateIncome:
    """Test income creation functionality"""

    @allure.title("Successful income creation")
    @allure.description("Verify that an income can be created with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_income_success(self, test_client, auth_headers):
        response = test_client.post("/api/income", json={
            "source": "Salary",
            "amount": 5000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["source"] == "Salary"
        assert response.json()["amount"] == 5000

    @allure.title("Income creation with missing source")
    @allure.description("Verify that income creation fails when source is missing")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_income_missing_source(self, test_client, auth_headers):
        response = test_client.post("/api/income", json={
            "amount": 5000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Income creation with missing amount")
    @allure.description("Verify that income creation fails when amount is missing")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_income_missing_amount(self, test_client, auth_headers):
        response = test_client.post("/api/income", json={
            "source": "Salary",
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Income creation with negative amount")
    @allure.description("Verify that income creation fails with negative amount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_income_negative_amount(self, test_client, auth_headers):
        response = test_client.post("/api/income", json={
            "source": "Salary",
            "amount": -100,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Income creation with zero amount")
    @allure.description("Verify that income creation fails with zero amount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_income_zero_amount(self, test_client, auth_headers):
        response = test_client.post("/api/income", json={
            "source": "Salary",
            "amount": 0,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Income creation with invalid date format")
    @allure.description("Verify that income creation fails with invalid date format")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_income_invalid_date(self, test_client, auth_headers):
        response = test_client.post("/api/income", json={
            "source": "Salary",
            "amount": 5000,
            "date": "invalid-date",
            "category": "Job"
        }, headers=auth_headers)
        
        assert response.status_code == 422

    @allure.title("Income creation without authentication")
    @allure.description("Verify that income creation fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_income_unauthorized(self, test_client):
        response = test_client.post("/api/income", json={
            "source": "Salary",
            "amount": 5000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        })
        
        assert response.status_code == 401


@allure.parent_suite("Backend API")
@allure.suite("Income")
@allure.feature("Income Management")
@allure.story("Get Income")
class TestGetIncome:
    """Test income retrieval functionality"""

    @allure.title("Get all income successfully")
    @allure.description("Verify that all income records can be retrieved for authenticated user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_income_success(self, test_client, auth_headers):
        # Create an income first
        test_client.post("/api/income", json={
            "source": "Salary",
            "amount": 5000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        response = test_client.get("/api/income", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

    @allure.title("Get income without authentication")
    @allure.description("Verify that income retrieval fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_income_unauthorized(self, test_client):
        response = test_client.get("/api/income")
        
        assert response.status_code == 401

    @allure.title("Get income returns empty list for new user")
    @allure.description("Verify that new user gets empty income list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_income_empty(self, test_client, auth_headers):
        response = test_client.get("/api/income", headers=auth_headers)
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 0


@allure.parent_suite("Backend API")
@allure.suite("Income")
@allure.feature("Income Management")
@allure.story("Update Income")
class TestUpdateIncome:
    """Test income update functionality"""

    @allure.title("Update income successfully")
    @allure.description("Verify that an income can be updated with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_income_success(self, test_client, auth_headers):
        # Create an income first
        create_response = test_client.post("/api/income", json={
            "source": "Salary",
            "amount": 5000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        income_id = create_response.json()["id"]
        
        # Update the income
        response = test_client.put(f"/api/income/{income_id}", json={
            "source": "Bonus",
            "amount": 6000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["source"] == "Bonus"
        assert response.json()["amount"] == 6000

    @allure.title("Update income with invalid ID")
    @allure.description("Verify that income update fails with non-existent ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_income_invalid_id(self, test_client, auth_headers):
        response = test_client.put("/api/income/99999", json={
            "source": "Bonus",
            "amount": 6000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        assert response.status_code == 404

    @allure.title("Update income without authentication")
    @allure.description("Verify that income update fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_income_unauthorized(self, test_client):
        response = test_client.put("/api/income/1", json={
            "source": "Bonus",
            "amount": 6000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        })
        
        assert response.status_code == 401


@allure.parent_suite("Backend API")
@allure.suite("Income")
@allure.feature("Income Management")
@allure.story("Delete Income")
class TestDeleteIncome:
    """Test income deletion functionality"""

    @allure.title("Delete income successfully")
    @allure.description("Verify that an income can be deleted")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_income_success(self, test_client, auth_headers):
        # Create an income first
        create_response = test_client.post("/api/income", json={
            "source": "Salary",
            "amount": 5000,
            "date": "2026-01-01T00:00:00",
            "category": "Job"
        }, headers=auth_headers)
        
        income_id = create_response.json()["id"]
        
        # Delete the income
        response = test_client.delete(f"/api/income/{income_id}", headers=auth_headers)
        
        assert response.status_code == 200

    @allure.title("Delete income with invalid ID")
    @allure.description("Verify that income deletion fails with non-existent ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_income_invalid_id(self, test_client, auth_headers):
        response = test_client.delete("/api/income/99999", headers=auth_headers)
        
        assert response.status_code == 404

    @allure.title("Delete income without authentication")
    @allure.description("Verify that income deletion fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_income_unauthorized(self, test_client):
        response = test_client.delete("/api/income/1")
        
        assert response.status_code == 401
