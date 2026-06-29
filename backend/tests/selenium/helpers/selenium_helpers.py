"""
Selenium helper utilities for test automation
Provides reusable methods for common Selenium operations
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure


class SeleniumHelper:
    """Helper class for common Selenium operations"""

    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = 10

    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_url_contains(self, text, timeout=None):
        """Wait for URL to contain specific text"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )

    def is_element_present(self, locator):
        """Check if element is present"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            return self.driver.find_element(*locator).is_displayed()
        except NoSuchElementException:
            return False

    def clear_and_send_keys(self, locator, text):
        """Clear field and send keys"""
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def click_element(self, locator):
        """Click on element"""
        element = self.wait_for_element_clickable(locator)
        element.click()

    def get_element_text(self, locator):
        """Get text from element"""
        element = self.wait_for_element(locator)
        return element.text

    def take_screenshot(self, name):
        """Take screenshot and attach to Allure"""
        screenshot_path = f"/tmp/{name}.png"
        self.driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot_path

    def attach_browser_logs(self):
        """Attach browser console logs to Allure"""
        logs = self.driver.get_log('browser')
        if logs:
            log_text = "\n".join([f"{log['level']}: {log['message']}" for log in logs])
            allure.attach(log_text, name="Browser Console Logs", attachment_type=allure.attachment_type.TEXT)

    def attach_page_source(self):
        """Attach page source to Allure"""
        allure.attach(self.driver.page_source, name="Page Source", attachment_type=allure.attachment_type.TEXT)

    def attach_current_url(self):
        """Attach current URL to Allure"""
        allure.attach(self.driver.current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT)

    def capture_failure_artifacts(self, test_name):
        """Capture all artifacts on test failure"""
        self.take_screenshot(f"{test_name}_failure")
        self.attach_browser_logs()
        self.attach_page_source()
        self.attach_current_url()

    def select_dropdown_by_value(self, locator, value):
        """Select dropdown option by value"""
        from selenium.webdriver.support.ui import Select
        element = self.wait_for_element(locator)
        select = Select(element)
        select.select_by_value(value)

    def select_dropdown_by_visible_text(self, locator, text):
        """Select dropdown option by visible text"""
        from selenium.webdriver.support.ui import Select
        element = self.wait_for_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)

    def execute_script(self, script, *args):
        """Execute JavaScript"""
        return self.driver.execute_script(script, *args)

    def scroll_to_element(self, locator):
        """Scroll to element"""
        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def wait_for_element_not_present(self, locator, timeout=None):
        """Wait for element to not be present"""
        timeout = timeout or self.default_timeout
        return WebDriverWait(self.driver, timeout).until_not(
            EC.presence_of_element_located(locator)
        )
