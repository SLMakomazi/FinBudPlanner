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


class LoginPage:
    """
    Page Object for Login Page
    
    Encapsulates all interactions with the login page following the
    Page Object Model (POM) design pattern for better maintainability.
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://localhost:4200/login"
        
    def load(self):
        """Navigate to login page"""
        self.driver.get(self.url)
        
    def enter_username(self, username):
        """
        Enter username in the username field
        Uses explicit wait to ensure element is present before interaction
        """
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(username)
        
    def enter_password(self, password):
        """
        Enter password in the password field
        Uses explicit wait to ensure element is present before interaction
        """
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys(password)
        
    def click_login(self):
        """
        Click the login button
        Uses explicit wait to ensure element is clickable before interaction
        """
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        
    def is_loaded(self):
        """
        Check if login page is loaded
        Returns True if username field is present, False otherwise
        """
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
    
    Encapsulates all interactions with the dashboard page following the
    Page Object Model (POM) design pattern for better maintainability.
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://localhost:4200/dashboard"
        
    def load(self):
        """Navigate to dashboard page"""
        self.driver.get(self.url)
        
    def is_loaded(self):
        """
        Check if dashboard page is loaded
        Returns True if dashboard container is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-container"))
            )
            return True
        except TimeoutException:
            return False
            
    def get_username(self):
        """
        Get the current username displayed on dashboard
        Returns the text content of the user info element
        """
        user_info = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".user-info"))
        )
        return user_info.text


class SeleniumRegressionTests(unittest.TestCase):
    """
    Selenium Regression Test Suite
    
    Contains functional regression tests for the FinBudPlanner application.
    All tests use headless Chrome mode for CI/CD compatibility.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up Chrome WebDriver with headless configuration
        Configured for GitHub Actions CI environment:
        - --headless=new: New headless mode (more stable than old headless)
        - --no-sandbox: Required for running in containers
        - --disable-dev-shm-usage: Prevents shared memory issues in containers
        - --disable-gpu: Disables GPU acceleration (not needed in headless)
        - --window-size: Sets viewport size for consistent rendering
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)  # Set implicit wait for all elements
        
    @classmethod
    def tearDownClass(cls):
        """Clean up WebDriver after all tests complete"""
        cls.driver.quit()
        
    def setUp(self):
        """Set up page objects for each test"""
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        
    def test_user_login(self):
        """
        Test user login functionality with a dynamic registration fallback
        for fresh/empty CI database container environments.
        
        Test Steps:
        1. Navigate to login page
        2. Attempt login with 'Siseko'
        3. If it times out or fails to redirect, navigate to /register
        4. Register the user 'Siseko'
        5. Return to login page, authenticate, and verify dashboard redirection
        """
        # Step 1: Navigate to login page
        self.login_page.load()
        self.assertTrue(self.login_page.is_loaded(), "Login page failed to load")
        
        # Step 2: Enter credentials
        self.login_page.enter_username("Siseko")
        self.login_page.enter_password("Makomazi@1958")
        
        # Submit login
        self.login_page.click_login()
        
        try:
            # Check if login succeeds immediately (user already exists)
            WebDriverWait(self.driver, 5).until(
                EC.url_contains("/dashboard")
            )
            print("User 'Siseko' already exists. Logged in successfully.")
        except TimeoutException:
            # Step 3: Login failed/timed out, meaning user does not exist in the fresh CI DB.
            # Navigate to the registration page (adjust URL path if needed)
            print("User 'Siseko' not found in fresh DB. Navigating to registration...")
            
            # Assuming your registration route is /register on the same host/port
            base_url = self.login_page.url.split("/login")[0]
            self.driver.get(f"{base_url}/register")
            
            # Step 4: Complete the registration form
            # (Ensure your registration inputs match these IDs or selectors)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            ).send_keys("Siseko")
            
            self.driver.find_element(By.ID, "password").send_keys("Makomazi@1958")
            
            # Click register submit button
            register_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            register_btn.click()
            
            # Step 5: Navigate back to login page to authenticate the newly created user
            self.login_page.load()
            self.assertTrue(self.login_page.is_loaded(), "Login page failed to reload after registration")
            
            self.login_page.enter_username("Siseko")
            self.login_page.enter_password("Makomazi@1958")
            self.login_page.click_login()
            
            # Final validation of the redirect sequence
            WebDriverWait(self.driver, 15).until(
                EC.url_contains("/dashboard")
            )
        
        # Verify dashboard is fully loaded and functional
        self.assertTrue(self.dashboard_page.is_loaded(), "Dashboard failed to load after login")
        
    def test_form_submission_workflow(self):
        """
        Test form submission workflow
        
        Test Steps:
        1. Login to application
        2. Navigate to income page
        3. Click add button to open form
        4. Fill form fields
        5. Submit form
        6. Verify form closes successfully
        """
        # First login
        self.login_page.load()
        self.assertTrue(self.login_page.is_loaded(), "Login page failed to load")
        
        self.login_page.enter_username("Siseko")
        self.login_page.enter_password("Makomazi@1958")
        self.login_page.click_login()
        
        # Wait for dashboard
        WebDriverWait(self.driver, 15).until(
            EC.url_contains("/dashboard")
        )
        self.assertTrue(self.dashboard_page.is_loaded(), "Dashboard failed to load")
        
        # Navigate to income page
        self.driver.get("http://localhost:4200/income")
        
        # Wait for income page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".budget-container"))
        )
        
        # Click "Set Budget" or "Add Income" button
        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
        )
        add_button.click()
        
        # Verify form appears
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".add-form"))
        )
        
        # Fill form fields
        source_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "source"))
        )
        source_field.send_keys("Test Income")
        
        amount_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "amount"))
        )
        amount_field.send_keys("1000")
        
        # Submit form
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-success"))
        )
        submit_button.click()
        
        # Verify success (form should close)
        WebDriverWait(self.driver, 10).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".add-form"))
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)
