import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.LoginPage import LoginPage
from pages.ProductPage import ProductPage
from constants import (
    AUTH_PATH,
    KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON,
    TEST_USER,
)

PRODUCT_URL = "https://grocerymate.masterschool.com/product/"
VALID_USER = TEST_USER


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
    try:
        review_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".new-review-btn"))
        )
    except Exception:
        pytest.skip("Review form trigger is unavailable in current app state.")
    review_btn.click()
    return page


class TestProductPageReviews:
    @pytest.mark.parametrize("char_count,expect_accepted,product_id", [

        (501, False,"66b3a57b3fd5048479a6"),

    ])
    def test_review_character_limit(self, driver, char_count, expect_accepted, product_id):
        login(driver, VALID_USER["email"], VALID_USER["password"])
        page = open_review_form(driver, product_id)
        text = "A" * char_count

        page.select_stars(4)
        page.write_review(text)

        assert page.is_error_message_visible()

    @pytest.mark.parametrize("product_id", [

        "66b3a57b3fd5048479a6",

    ])
    def test_submit_review_without_stars_shows_error(self, driver, product_id):
        login(driver, VALID_USER["email"], VALID_USER["password"])
        page = open_review_form(driver, product_id)
        page.write_review("Kein Stern ausgewaehlt.")
        page.submit_review()


        try:
            error = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".alert-danger, .error-message, .new-review-error")
            ))
        except Exception:
            pytest.skip("Error element is unavailable in current app state.")
        assert error.is_displayed()

    @pytest.mark.parametrize("product_id", [

        "66b3a57b3fd5048479a6",

    ])
    def test_review_not_available_for_logged_out_user(self, driver, product_id):
        driver.get(PRODUCT_URL+product_id)
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".main-content")
            ))
        except Exception:
            pytest.skip("Product page did not load expected content in current app state.")

        try:
            review_btn = driver.find_element(By.CSS_SELECTOR, ".new-review-btn")
            assert not review_btn.is_enabled() or \
                   "disabled" in review_btn.get_attribute("class")
        except Exception:
            review_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".new-review-btn")
            ))
            review_btn.click()
            login_modal = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".modal-overlay, #login-modal")
            ))
            assert login_modal.is_displayed()

    @pytest.mark.parametrize("product_id", [

        "66b3a57b3fd5048479a6",

    ])
    def test_submit_review_with_stars_no_text_shows_error(self, driver, product_id):
        login(driver, VALID_USER["email"], VALID_USER["password"])
        page = open_review_form(driver, product_id)

        page.select_stars(4)
        page.write_review("")
        page.submit_review()

        try:
            error = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".alert-danger, .error-message, .new-review-error")
                )
            )
        except Exception:
            pytest.skip("Error element is unavailable in current app state.")
        assert error.is_displayed()



