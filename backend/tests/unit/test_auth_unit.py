"""
Unit tests for Authentication module
Tests validation, error handling, and edge cases
"""
import pytest
from fastapi.testclient import TestClient
from main import app
import allure


@allure.parent_suite("Backend API")
@allure.suite("Authentication")
@allure.feature("Authentication")
@allure.story("User Registration")
class TestUserRegistration:
    """Test user registration functionality"""

    @allure.title("Successful user registration")
    @allure.description("Verify that a new user can be registered with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_success(self, test_client):
        response = test_client.post("/api/register", json={
            "username": "newuser",
            "password": "ValidPass123!"
        })
        assert response.status_code == 200
        assert "id" in response.json()
        assert response.json()["username"] == "newuser"

    @allure.title("Registration with duplicate username")
    @allure.description("Verify that duplicate username registration fails appropriately")
    @allure.severity(allure.severity_level.HIGH)
    def test_register_duplicate_username(self, test_client, test_user):
        # First registration
        test_client.post("/api/register", json=test_user)
        
        # Duplicate registration
        response = test_client.post("/api/register", json=test_user)
        assert response.status_code == 400

    @allure.title("Registration with invalid password - too short")
    @allure.description("Verify that registration fails with password shorter than 8 characters")
    @allure.severity(allure.severity_level.HIGH)
    def test_register_invalid_password_short(self, test_client):
        response = test_client.post("/api/register", json={
            "username": "user1",
            "password": "Short1!"
        })
        assert response.status_code == 422

    @allure.title("Registration with invalid password - no special character")
    @allure.description("Verify that registration fails with password lacking special characters")
    @allure.severity(allure.severity_level.HIGH)
    def test_register_invalid_password_no_special(self, test_client):
        response = test_client.post("/api/register", json={
            "username": "user2",
            "password": "Password123"
        })
        assert response.status_code == 422

    @allure.title("Registration with missing username")
    @allure.description("Verify that registration fails when username is missing")
    @allure.severity(allure.severity_level.HIGH)
    def test_register_missing_username(self, test_client):
        response = test_client.post("/api/register", json={
            "password": "ValidPass123!"
        })
        assert response.status_code == 422

    @allure.title("Registration with missing password")
    @allure.description("Verify that registration fails when password is missing")
    @allure.severity(allure.severity_level.HIGH)
    def test_register_missing_password(self, test_client):
        response = test_client.post("/api/register", json={
            "username": "user3"
        })
        assert response.status_code == 422

    @allure.title("Registration with empty username")
    @allure.description("Verify that registration fails with empty username")
    @allure.severity(allure.severity_level.HIGH)
    def test_register_empty_username(self, test_client):
        response = test_client.post("/api/register", json={
            "username": "",
            "password": "ValidPass123!"
        })
        assert response.status_code == 422

    @allure.title("Registration with empty password")
    @allure.description("Verify that registration fails with empty password")
    @allure.severity(allure.severity_level.HIGH)
    def test_register_empty_password(self, test_client):
        response = test_client.post("/api/register", json={
            "username": "user4",
            "password": ""
        })
        assert response.status_code == 422


@allure.parent_suite("Backend API")
@allure.suite("Authentication")
@allure.feature("Authentication")
@allure.story("User Login")
class TestUserLogin:
    """Test user login functionality"""

    @allure.title("Successful user login")
    @allure.description("Verify that a registered user can login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, test_client, test_user):
        # Register user first
        test_client.post("/api/register", json=test_user)
        
        # Login
        response = test_client.post("/api/token", data={
            "username": test_user["username"],
            "password": test_user["password"]
        })
        
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()

    @allure.title("Login with invalid username")
    @allure.description("Verify that login fails with non-existent username")
    @allure.severity(allure.severity_level.HIGH)
    def test_login_invalid_username(self, test_client):
        response = test_client.post("/api/token", data={
            "username": "nonexistent",
            "password": "ValidPass123!"
        })
        assert response.status_code == 401

    @allure.title("Login with invalid password")
    @allure.description("Verify that login fails with incorrect password")
    @allure.severity(allure.severity_level.HIGH)
    def test_login_invalid_password(self, test_client, test_user):
        # Register user first
        test_client.post("/api/register", json=test_user)
        
        # Login with wrong password
        response = test_client.post("/api/token", data={
            "username": test_user["username"],
            "password": "WrongPass123!"
        })
        assert response.status_code == 401

    @allure.title("Login with missing username")
    @allure.description("Verify that login fails when username is missing")
    @allure.severity(allure.severity_level.HIGH)
    def test_login_missing_username(self, test_client):
        response = test_client.post("/api/token", data={
            "password": "ValidPass123!"
        })
        assert response.status_code == 422

    @allure.title("Login with missing password")
    @allure.description("Verify that login fails when password is missing")
    @allure.severity(allure.severity_level.HIGH)
    def test_login_missing_password(self, test_client):
        response = test_client.post("/api/token", data={
            "username": "user1"
        })
        assert response.status_code == 422

    @allure.title("Login with empty credentials")
    @allure.description("Verify that login fails with empty username and password")
    @allure.severity(allure.severity_level.HIGH)
    def test_login_empty_credentials(self, test_client):
        response = test_client.post("/api/token", data={
            "username": "",
            "password": ""
        })
        assert response.status_code == 422
