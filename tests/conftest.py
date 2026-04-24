import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.LoginPage import LoginPage
from pages.ShoppingCartPage import ShoppingCartPage
from selenium.webdriver.chrome.options import Options
from constants import (
    AUTH_PATH,
    AUTH_URL,
    KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
)


@pytest.fixture(scope="function")
def driver():
    """Driver."""
    options = Options()

    # --- SETUP ---
    # Disable Chrome's password manager and credential service popups
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # Hide automation flags to make the browser look more like a regular user
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Configure browser capabilities: disable popups/notifications and start maximized
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")

    # Use incognito mode to ensure a fresh session without cached data
    options.add_argument("--incognito")

    # Initialize the WebDriver using the specified path or default system path
    driver_path = os.getenv("CHROMEDRIVER_PATH")
    if driver_path:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    # Clear all cookies to prevent session leakage between test
    driver.delete_all_cookies()

    # Set a global fallback wait time for element discovery
    driver.implicitly_wait(5)

    # Provide the driver instance to the test
    yield driver

    # --- TEARDOWN ---
    # Close the browser and end the session
    driver.quit()


@pytest.fixture()
def logged_in(driver):
    """Logs in the user using the LoginPage (Strict POM approach)."""
    # Initialize the login page and navigate to the authentication URL
    login_page = LoginPage(driver)
    login_page.open(AUTH_URL)
    # Perform login using test credentials
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    # Skip tests if the account is unavailable to prevent false negatives
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)

    return driver


@pytest.fixture()
def cleared_cart(driver, logged_in):
    """Ensures the shopping cart is empty before starting a test."""
    # Navigate to the cart and remove any existing items for a clean state
    cart_page = ShoppingCartPage(driver)
    cart_page.open_cart()
    cart_page.remove_all_items()

    return cart_page
