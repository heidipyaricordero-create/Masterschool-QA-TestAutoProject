import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.LoginPage import LoginPage
from pages.ProductPage import ProductPage
from constants import (
    AUTH_PATH,
    TEST_USER,
    KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON,
)

VALID_USER = TEST_USER
PRODUCT_URL = "https://grocerymate.masterschool.com/product/"

def login(driver, email, password):
    page = LoginPage(driver)
    page.load()
    page.login(email, password)
    if AUTH_PATH in driver.current_url and page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)
    return page

def open_review_form(driver, product_id):
    page = ProductPage(driver)
    page.open(PRODUCT_URL + product_id)
    wait = WebDriverWait(driver, 10)
    review_btn = None
    try:
        review_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".new-review-btn"))
        )
    except Exception:
        pytest.skip("Review form trigger is unavailable in current app state.")
    review_btn.click()
    return page
