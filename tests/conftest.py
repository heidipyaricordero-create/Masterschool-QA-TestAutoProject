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
    CART_URL,
    KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
)


@pytest.fixture(scope="function")
def driver():
    options = Options()


    # 1. Deaktiviert den Passwort-Manager und den Breach-Check
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)


    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")


    options.add_argument("--incognito")

    driver_path = os.getenv("CHROMEDRIVER_PATH")
    if driver_path:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.delete_all_cookies()

    # Implicit Wait ist okay, aber wir verlassen uns primär auf Explicit Waits in den Pages
    driver.implicitly_wait(5)

    yield driver
    driver.quit()


@pytest.fixture()
def logged_in(driver):
    """Loggt den User ein, indem die LoginPage genutzt wird (Strenges POM)."""
    login_page = LoginPage(driver)
    login_page.open(AUTH_URL)

    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)


    return driver


@pytest.fixture()
def cleared_cart(driver, logged_in):

    cart_page = ShoppingCartPage(driver)
    cart_page.open_cart()
    cart_page.remove_all_items()
    return cart_page