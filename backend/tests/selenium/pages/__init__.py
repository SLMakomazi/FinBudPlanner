"""
Page Object Model package
"""
from .base_page import BasePage
from .login_page import LoginPage
from .signup_page import SignupPage
from .dashboard_page import DashboardPage

__all__ = ['BasePage', 'LoginPage', 'SignupPage', 'DashboardPage']
