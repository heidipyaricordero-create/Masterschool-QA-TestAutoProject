from datetime import date, timedelta
from pages.AgeVerificationPage import AgeVerificationPage
from pages.HomePage import HomePage
from pages.LoginPage import LoginPage
import pytest
from constants import (
    ADULT_DATE_OF_BIRTH,
    AUTH_PATH,
    CELERY_PRODUCT_URL,
    KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
)

def test_valid_age_logged_in_users(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)

    homepage = HomePage(driver)
    homepage.go_to_shop()

    age_verification_modal = AgeVerificationPage(driver)
    age_verification_modal.verify_age(ADULT_DATE_OF_BIRTH)

    assert age_verification_modal.is_age_success_displayed()

def _date_18_years_ago() -> date:
    today = date.today()
    try:
        return today.replace(year=today.year - 18)
    except ValueError:
        # Handles leap-day birthdays in non-leap years.
        return today.replace(month=2, day=28, year=today.year - 18)


def test_user_exactly_18_years_old_today(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)

    homepage = HomePage(driver)
    homepage.go_to_shop()

    age_verification_modal = AgeVerificationPage(driver)
    birthdate_18_years_ago = _date_18_years_ago().strftime("%d-%m-%Y")
    age_verification_modal.verify_age(birthdate_18_years_ago)

    assert age_verification_modal.is_age_success_displayed()


def test_user_one_day_younger_than_18(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)

    homepage = HomePage(driver)
    homepage.go_to_shop()

    age_verification_modal = AgeVerificationPage(driver)
    birthdate_one_day_too_young = (_date_18_years_ago() + timedelta(days=1)).strftime(
        "%d-%m-%Y"
    )
    age_verification_modal.verify_age(birthdate_one_day_too_young)

    assert age_verification_modal.is_underage_alert_displayed()


def test_direct_url_bypasses_verification(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)

    driver.get(CELERY_PRODUCT_URL)
    age_verification_modal = AgeVerificationPage(driver)
    age_verification_modal.verify_age(ADULT_DATE_OF_BIRTH)

    assert age_verification_modal.is_age_success_displayed()

