import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.ProductPage import ProductPage

PRODUCT_URL = "https://grocerymate.masterschool.com/store/product/celery"
VALID_USER  = {"email": "johndoe@example.com", "password": "admin123"}


def login(driver, email, password):
    driver.get("https://grocerymate.masterschool.com/login")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.url_contains("/store"))


def open_review_form(driver):
    driver.get(PRODUCT_URL)
    wait = WebDriverWait(driver, 10)
    review_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".new-review-btn"))
    )
    review_btn.click()
    return ProductPage(driver)


class TestProductPageReviews:
    @pytest.mark.parametrize("char_count,expect_accepted", [
        (500,True),
        (5001, False),
    ])
    def test_review_character_limit(self, driver, char_count, expect_accepted):
        login(driver, VALID_USER["email"], VALID_USER["password"])
        page = open_review_form(driver)
        text = "A" * char_count

        page.select_stars(4)
        page.write_review(text)
        page.submit_review()

        wait = WebDriverWait(driver, 10)
        textarea = driver.find_element(By.CSS_SELECTOR, "textarea.new-review-form-control")

        if expect_accepted:
            wait.until(EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "textarea.new-review-form-control")
            ))
            comments = driver.find_element(By.CSS_SELECTOR, ".product-comments")
            assert text[:20] in comments.text
        else:
            actual_length = len(textarea.get_attribute("value"))
            assert actual_length <= 500

    def test_average_rating_rounds_correctly(self, driver):
        ratings = [4, 5, 4]

        for stars in ratings:
            login(driver, VALID_USER["email"], VALID_USER["password"])
            page = open_review_form(driver)
            page.select_stars(stars)
            page.write_review(f"Testbewertung mit {stars} Sternen.")
            page.submit_review()
            driver.get("https://grocerymate.masterschool.com/logout")

        login(driver, VALID_USER["email"], VALID_USER["password"])
        driver.get(PRODUCT_URL)

        wait = WebDriverWait(driver, 10)
        avg_display = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".average-rating, #average-rating")
        ))
        avg_value = float(avg_display.text.replace(",", "."))
        assert avg_value == pytest.approx(4.5, abs=0.1)

    def test_submit_review_without_stars_shows_error(self, driver):
        login(driver, VALID_USER["email"], VALID_USER["password"])
        page = open_review_form(driver)

        page.write_review("Kein Stern ausgewaehlt.")
        page.submit_review()

        wait = WebDriverWait(driver, 10)
        error = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".alert-danger, .error-message, .new-review-error")
        ))
        assert error.is_displayed()

    def test_review_not_available_for_logged_out_user(self, driver):
        driver.get(PRODUCT_URL)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".main-content")
        ))

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
