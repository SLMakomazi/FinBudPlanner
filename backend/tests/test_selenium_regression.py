"""
Selenium Regression Test Suite for FinBudPlanner
Uses Page Object Model (POM) pattern for maintainable test structure

This test suite automates functional regression testing of the web application
using Selenium WebDriver with Chrome in headless mode for CI/CD environments.
"""

import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ==============================================================================
# GLOBAL TEST CONFIGURATION
# ==============================================================================
BASE_URL = "http://localhost:4200"
TEST_USER = "Siseko"
TEST_PASS = "Makomazi1958"


class LoginPage:
    """
    Page Object for Login Page
    Encapsulates all interactions with the login page following the POM pattern.
    """
    def __init__(self, driver):
        self.driver = driver
        self.url = f"{BASE_URL}/login"
        
    def load(self):
        self.driver.get(self.url)
        
    def enter_username(self, username):
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(username)
        
    def enter_password(self, password):
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys(password)
        
    def click_login(self):
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        
    def is_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            return True
        except TimeoutException:
            return False


class DashboardPage:
    """
    Page Object for Dashboard Page
    Encapsulates all interactions with the dashboard page following the POM pattern.
    """
    def __init__(self, driver):
        self.driver = driver
        self.url = f"{BASE_URL}/dashboard"
        
    def load(self):
        self.driver.get(self.url)
        
    def is_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-container"))
            )
            return True
        except TimeoutException:
            return False
            
    def get_username(self):
        user_info = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info"))
        )
        return user_info.text


class SeleniumRegressionTests(unittest.TestCase):
    """
    Selenium Regression Test Suite
    Contains functional regression tests for the FinBudPlanner application.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up Chrome WebDriver with headless configuration for CI/CD environments"""
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        
    def setUp(self):
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)

    def _login_workflow(self):
        """Reusable login helper flow that triggers registration fallback if needed"""
        self.login_page.load()
        self.assertTrue(self.login_page.is_loaded(), "Login page failed to load")
        
        self.login_page.enter_username(TEST_USER)
        self.login_page.enter_password(TEST_PASS)
        self.login_page.click_login()
        
        try:
            WebDriverWait(self.driver, 5).until(EC.url_contains("/dashboard"))
        except TimeoutException:
            print(f"User '{TEST_USER}' not found in fresh DB. Falling back to registration...")
            
            # Navigate to dynamic signup variants safely
            self.driver.get(f"{BASE_URL}/register")
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
            except TimeoutException:
                self.driver.get(f"{BASE_URL}/signup")
            
            # Fill out the HTML template input fields precisely by ID
            reg_username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            reg_username.clear()
            reg_username.send_keys(TEST_USER)
            
            reg_password = self.driver.find_element(By.ID, "password")
            reg_password.clear()
            reg_password.send_keys(TEST_PASS)
            
            # Satisfy Angular client-side registration form logic rules
            reg_confirm = self.driver.find_element(By.ID, "confirmPassword")
            reg_confirm.clear()
            reg_confirm.send_keys(TEST_PASS)
            
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            ).click()
            
            # Complete redirect tracking chain back to login validation
            WebDriverWait(self.driver, 10).until(lambda d: "/dashboard" in d.current_url or "/login" in d.current_url)
            
            if "/dashboard" not in self.driver.current_url:
                self.login_page.load()
                self.login_page.enter_username(TEST_USER)
                self.login_page.enter_password(TEST_PASS)
                self.login_page.click_login()
            
            WebDriverWait(self.driver, 15).until(EC.url_contains("/dashboard"))
        
    def test_user_login(self):
        """Test user login functionality with a dynamic registration fallback"""
        self._login_workflow()
        self.assertTrue(self.dashboard_page.is_loaded(), "Dashboard failed to load after login")
        
    def test_form_submission_workflow(self):
        """Test form submission workflow on the income view layer"""
        # Execute login cycle
        self._login_workflow()
        self.assertTrue(self.dashboard_page.is_loaded(), "Dashboard failed to load")
        
        # Navigate directly to income dashboard module
        self.driver.get(f"{BASE_URL}/income")
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".budget-container"))
        )
        
        # Open targeted configuration form context
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
        ).click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".add-form"))
        )
        
        # Populate operational values
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "source"))
        ).send_keys("Test Income")
        
        self.driver.find_element(By.ID, "amount").send_keys("1000")
        
        # Submit transaction details safely
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-success"))
        ).click()
        
        # Verify component state cleanup changes match form removal expectation
        WebDriverWait(self.driver, 10).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".add-form"))
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)