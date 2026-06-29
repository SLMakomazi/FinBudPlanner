"""
Selenium UI Regression Tests - Income Workflow
Tests income management functionality with Page Object Model and Allure reporting
"""
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tests.selenium.pages.login_page import LoginPage
from tests.selenium.pages.signup_page import SignupPage
from tests.selenium.pages.dashboard_page import DashboardPage
from selenium.common.exceptions import TimeoutException


BASE_URL = "http://localhost:4200"
TEST_USER = "Siseko"
TEST_PASS = "Makomazi!1958"


@allure.parent_suite("Frontend UI")
@allure.suite("Selenium UI")
@allure.feature("Income Management")
@allure.story("Income Workflow")
class TestIncomeWorkflow:
    """Selenium tests for income management workflow"""

    @pytest.fixture(scope="class")
    def driver(self):
        """Setup Chrome WebDriver with headless configuration"""
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    @pytest.fixture
    def login_page(self, driver):
        """Initialize login page"""
        return LoginPage(driver, BASE_URL)

    @pytest.fixture
    def signup_page(self, driver):
        """Initialize signup page"""
        return SignupPage(driver, BASE_URL)

    @pytest.fixture
    def dashboard_page(self, driver):
        """Initialize dashboard page"""
        return DashboardPage(driver, BASE_URL)

    def login_workflow(self, login_page, signup_page):
        """
        Complete login workflow with registration fallback
        """
        login_page.load()
        assert login_page.is_loaded(), "Login page failed to load"
        
        login_page.login(TEST_USER, TEST_PASS)
        
        try:
            login_page.helper.wait_for_url_contains("/dashboard", timeout=5)
        except TimeoutException:
            allure.step("User not found, attempting registration fallback")
            
            signup_page.load()
            if not signup_page.is_loaded():
                signup_page.load_alternative()
            
            signup_page.signup(TEST_USER, TEST_PASS)
            
            if signup_page.is_error_message_displayed():
                allure.attach(signup_page.get_error_message(), name="Registration Error",
                             attachment_type=allure.attachment_type.TEXT)
                login_page.load()
                login_page.login(TEST_USER, TEST_PASS)
            
            login_page.helper.wait_for_url_contains("/dashboard", timeout=10)
            
            if "/dashboard" not in login_page.get_current_url():
                login_page.load()
                login_page.login(TEST_USER, TEST_PASS)
                login_page.helper.wait_for_url_contains("/dashboard", timeout=15)

    @allure.title("Selenium - Income form submission workflow")
    @allure.description("Test complete income creation workflow including login, navigation, and form submission")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_income_workflow(self, driver, login_page, signup_page, dashboard_page):
        """Test income form submission workflow"""
        try:
            # Login
            self.login_workflow(login_page, signup_page)
            
            # Navigate to income section
            dashboard_page.navigate_to_income()
            login_page.helper.wait_for_url_contains("/income")
            
            # Verify income container is loaded
            income_container = (By.CSS_SELECTOR, ".income-container")
            login_page.helper.wait_for_element(income_container)
            
            # Add income using the workflow
            dashboard_page.add_income(
                source="Test Income",
                amount=1000,
                date="2026-06-27",
                category="salary"
            )
            
            # Check for error alerts
            error_alert = (By.CSS_SELECTOR, ".add-form .alert-danger")
            if login_page.helper.is_element_visible(error_alert):
                error_text = login_page.helper.get_element_text(error_alert)
                allure.attach(error_text, name="Backend Validation Error",
                             attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"Backend validation failed: {error_text}")
            
        except Exception as e:
            login_page.helper.capture_failure_artifacts("test_income_workflow")
            raise
