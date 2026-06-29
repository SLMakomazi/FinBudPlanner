"""
Signup Page Object Model
Encapsulates all interactions with the signup page
"""
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
import allure


class SignupPage(BasePage):
    """Page Object for Signup Page"""

    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirmPassword")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, ".add-form button[type='submit'], button[type='submit']")
    ALERT_DANGER = (By.CSS_SELECTOR, ".alert-danger")

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url
        self.url = f"{base_url}/register"

    def load(self):
        """Navigate to signup page"""
        self.navigate_to(self.url)
        self.wait_for_page_load()

    def load_alternative(self):
        """Navigate to alternative signup URL"""
        self.navigate_to(f"{self.base_url}/signup")
        self.wait_for_page_load()

    def enter_username(self, username):
        """Enter username in the username field"""
        self.helper.clear_and_send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """Enter password in the password field"""
        self.helper.clear_and_send_keys(self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, password):
        """Enter password in the confirm password field"""
        self.helper.clear_and_send_keys(self.CONFIRM_PASSWORD_INPUT, password)

    def click_submit(self):
        """Click the submit button"""
        self.helper.click_element(self.SUBMIT_BUTTON)

    def signup(self, username, password):
        """Perform complete signup action"""
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.click_submit()

    def is_loaded(self):
        """Check if signup page is loaded"""
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
