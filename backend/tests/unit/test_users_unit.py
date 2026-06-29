"""
Unit tests for Users module
Tests validation, error handling, and edge cases
"""
import pytest
from fastapi.testclient import TestClient
from main import app
import allure


@allure.parent_suite("Backend API")
@allure.suite("Users")
@allure.feature("User Management")
@allure.story("Get Current User")
class TestGetCurrentUser:
    """Test current user retrieval functionality"""

    @allure.title("Get current user successfully")
    @allure.description("Verify that authenticated user can retrieve their profile")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_me_success(self, test_client, auth_headers):
        response = test_client.get("/api/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        assert "username" in response.json()
        assert "id" in response.json()

    @allure.title("Get current user without authentication")
    @allure.description("Verify that user profile retrieval fails without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_me_unauthorized(self, test_client):
        response = test_client.get("/api/users/me")
        
        assert response.status_code == 401

    @allure.title("Get current user returns correct username")
    @allure.description("Verify that returned username matches authenticated user")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_me_correct_username(self, test_client, test_user, auth_headers):
        response = test_client.get("/api/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["username"] == test_user["username"]


@allure.parent_suite("Backend API")
@allure.suite("Users")
@allure.feature("User Management")
@allure.story("User Profile Validation")
class TestUserProfileValidation:
    """Test user profile validation"""

    @allure.title("User profile contains required fields")
    @allure.description("Verify that user profile contains all required fields")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_profile_required_fields(self, test_client, auth_headers):
        response = test_client.get("/api/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "username" in data
        assert isinstance(data["id"], int)
        assert isinstance(data["username"], str)

    @allure.title("User profile username is not empty")
    @allure.description("Verify that username field is not empty")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_profile_username_not_empty(self, test_client, auth_headers):
        response = test_client.get("/api/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["username"]) > 0
