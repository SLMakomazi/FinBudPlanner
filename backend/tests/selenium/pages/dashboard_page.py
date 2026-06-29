"""
Dashboard Page Object Model
Encapsulates all interactions with the dashboard page
"""
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
import allure


class DashboardPage(BasePage):
    """Page Object for Dashboard Page"""

    # Locators
    DASHBOARD_CONTAINER = (By.CSS_SELECTOR, ".dashboard-container")
    INCOME_BUTTON = (By.CSS_SELECTOR, ".btn-primary")
    ADD_FORM = (By.CSS_SELECTOR, ".add-form")
    SOURCE_INPUT = (By.ID, "source")
    AMOUNT_INPUT = (By.ID, "amount")
    DATE_INPUT = (By.ID, "date")
    CATEGORY_SELECT = (By.ID, "category")

    def __init__(self, driver, base_url):
        super().__init__(driver)
        self.base_url = base_url
        self.url = f"{base_url}/dashboard"

    def load(self):
        """Navigate to dashboard page"""
        self.navigate_to(self.url)
        self.wait_for_page_load()

    def is_loaded(self):
        """Check if dashboard page is loaded"""
        try:
            self.helper.wait_for_element(self.DASHBOARD_CONTAINER)
            return True
        except TimeoutException:
            return False

    def navigate_to_income(self):
        """Navigate to income section"""
        self.navigate_to(f"{self.base_url}/income")
        self.wait_for_page_load()

    def navigate_to_expense(self):
        """Navigate to expense section"""
        self.navigate_to(f"{self.base_url}/expense")
        self.wait_for_page_load()

    def navigate_to_budget(self):
        """Navigate to budget section"""
        self.navigate_to(f"{self.base_url}/budget")
        self.wait_for_page_load()

    def click_add_button(self):
        """Click the add button to open form"""
        self.helper.click_element(self.INCOME_BUTTON)

    def is_form_displayed(self):
        """Check if add form is displayed"""
        return self.helper.is_element_visible(self.ADD_FORM)

    def enter_source(self, source):
        """Enter source in income form"""
        self.helper.clear_and_send_keys(self.SOURCE_INPUT, source)

    def enter_amount(self, amount):
        """Enter amount in income form"""
        self.helper.clear_and_send_keys(self.AMOUNT_INPUT, str(amount))

    def enter_date(self, date):
        """Enter date in income form using JavaScript to bypass headless issues"""
        date_input = self.helper.wait_for_element(self.DATE_INPUT)
        self.helper.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
            date_input,
            date
        )

    def select_category(self, value):
        """Select category from dropdown"""
        self.helper.select_dropdown_by_value(self.CATEGORY_SELECT, value)

    def submit_form(self):
        """Submit the add form"""
        submit_button = (By.CSS_SELECTOR, ".add-form button[type='submit']")
        self.helper.click_element(submit_button)

    def wait_for_form_to_close(self):
        """Wait for the form to close after submission"""
        self.helper.wait_for_element_not_present(self.ADD_FORM, timeout=15)

    def add_income(self, source, amount, date, category):
        """Complete workflow to add income"""
        self.click_add_button()
        self.helper.wait_for_element(self.ADD_FORM)
        self.enter_source(source)
        self.enter_amount(amount)
        self.enter_date(date)
        self.select_category(category)
        self.submit_form()
        self.wait_for_form_to_close()
