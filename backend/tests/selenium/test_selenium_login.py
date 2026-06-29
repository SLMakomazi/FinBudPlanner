"""
Selenium UI Regression Tests - User Login Workflow
Tests user login functionality with Page Object Model and Allure reporting
"""
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.dashboard_page import DashboardPage


BASE_URL = "http://localhost:4200"
TEST_USER = "Siseko"
TEST_PASS = "Makomazi!1958"


@allure.parent_suite("Frontend UI")
@allure.suite("Selenium UI")
@allure.feature("User Authentication")
@allure.story("User Login")
class TestUserLogin:
    """Selenium tests for user login workflow"""

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

    def login_workflow(self, login_page, signup_page, dashboard_page):
        """
        Complete login workflow with registration fallback
        Handles both successful login and registration scenarios
        """
        login_page.load()
        assert login_page.is_loaded(), "Login page failed to load"
        
        login_page.login(TEST_USER, TEST_PASS)
        
        try:
            # Check if login works immediately
            login_page.helper.wait_for_url_contains("/dashboard", timeout=5)
        except TimeoutException:
            allure.step("User not found, attempting registration fallback")
            
            # Navigate to signup page
            signup_page.load()
            if not signup_page.is_loaded():
                signup_page.load_alternative()
            
            # Fill out signup form
            signup_page.signup(TEST_USER, TEST_PASS)
            
            # Check for error message (user already exists)
            if signup_page.is_error_message_displayed():
                allure.attach(signup_page.get_error_message(), name="Registration Error", 
                             attachment_type=allure.attachment_type.TEXT)
                allure.step("User already exists, switching to login")
                
                # Click login link
                login_page.load()
                login_page.login(TEST_USER, TEST_PASS)
            
            # Wait for redirect
            login_page.helper.wait_for_url_contains("/dashboard", timeout=10)
            
            # If not on dashboard, try login again
            if "/dashboard" not in login_page.get_current_url():
                login_page.load()
                login_page.login(TEST_USER, TEST_PASS)
                login_page.helper.wait_for_url_contains("/dashboard", timeout=15)

    @allure.title("Selenium - User login with registration fallback")
    @allure.description("Test user login functionality with automatic registration fallback if user doesn't exist")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_user_login(self, driver, login_page, signup_page, dashboard_page):
        """Test user login with registration fallback"""
        try:
            self.login_workflow(login_page, signup_page, dashboard_page)
            dashboard_page.load()
            assert dashboard_page.is_loaded(), "Dashboard failed to load after login"
        except Exception as e:
            login_page.helper.capture_failure_artifacts("test_user_login")
            raise
