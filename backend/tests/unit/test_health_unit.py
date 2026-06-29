"""
Unit tests for Health endpoint
Tests validation, error handling, and edge cases
"""
import pytest
from fastapi.testclient import TestClient
from main import app
import allure


@allure.parent_suite("Backend API")
@allure.suite("Health")
@allure.feature("Health Check")
@allure.story("Health Endpoint")
class TestHealthEndpoint:
    """Test health check endpoint functionality"""

    @allure.title("Health check returns 200 status")
    @allure.description("Verify that health endpoint returns HTTP 200 status")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_health_check_status(self, test_client):
        response = test_client.get("/health")
        
        assert response.status_code == 200

    @allure.title("Health check returns healthy status")
    @allure.description("Verify that health endpoint returns healthy status in JSON")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_health_check_returns_healthy_status(self, test_client):
        response = test_client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    @allure.title("Health check response is JSON")
    @allure.description("Verify that health endpoint returns valid JSON content type")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_health_check_content_type(self, test_client):
        response = test_client.get("/health")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    @allure.title("Health check response structure")
    @allure.description("Verify that health endpoint returns correct JSON structure")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_health_check_structure(self, test_client):
        response = test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "status" in data
        assert isinstance(data["status"], str)

    @allure.title("Health check does not require authentication")
    @allure.description("Verify that health endpoint is accessible without authentication")
    @allure.severity(allure.severity_level.MEDIUM)
    def test_health_check_no_auth_required(self, test_client):
        response = test_client.get("/health")
        
        assert response.status_code == 200
