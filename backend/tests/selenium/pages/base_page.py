"""
Base Page Object Model class
Provides common functionality for all page objects
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .helpers.selenium_helpers import SeleniumHelper
import allure


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver):
        self.driver = driver
        self.helper = SeleniumHelper(driver)
        self.timeout = 10

    def navigate_to(self, url):
        """Navigate to specific URL"""
        self.driver.get(url)

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url

    def get_title(self):
        """Get page title"""
        return self.driver.title

    def wait_for_page_load(self):
        """Wait for page to load"""
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def is_loaded(self):
        """Check if page is loaded - to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement is_loaded method")
