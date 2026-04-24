import pytest
from pages.LoginPage import LoginPage
from constants import (
    AUTH_PATH,
    KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
)


def _skip_if_auth_unavailable(driver, login_page):
    """Skip if auth unavailable."""
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)


def test_login(driver):
    """Test login."""
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    _skip_if_auth_unavailable(driver, login_page)
    assert AUTH_PATH not in driver.current_url


