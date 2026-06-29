"""
Login Page Object Model
Encapsulates all interactions with the login page
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
import allure


class LoginPage(BasePage):
    """Page Object for Login Page"""

    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_HERE_LINK = (By.LINK_TEXT, "Login here")
    ALERT_DANGER = (By.CSS_SELECTOR, ".alert-danger")

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url
        self.url = f"{base_url}/login"

    def load(self):
        """Navigate to login page"""
        self.navigate_to(self.url)
        self.wait_for_page_load()

    def enter_username(self, username):
        """Enter username in the username field"""
        self.helper.clear_and_send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Enter password in the password field"""
        self.helper.clear_and_send_keys(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Click the login button"""
        self.helper.click_element(self.SUBMIT_BUTTON)

    def login(self, username, password):
        """Perform complete login action"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def is_loaded(self):
        """Check if login page is loaded"""
        try:
            self.helper.wait_for_element(self.USERNAME_INPUT)
            return True
        except TimeoutException:
            return False

    def is_error_message_displayed(self):
        """Check if error message is displayed"""
        return self.helper.is_element_visible(self.ALERT_DANGER)

    def get_error_message(self):
        """Get error message text"""
        if self.is_error_message_displayed():
            return self.helper.get_element_text(self.ALERT_DANGER)
        return None

    def click_login_here_link(self):
        """Click the 'Login here' link"""
        self.helper.click_element(self.LOGIN_HERE_LINK)
