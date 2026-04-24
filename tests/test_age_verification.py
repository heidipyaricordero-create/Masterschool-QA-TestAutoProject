from datetime import date, timedelta
from pages.AgeVerificationPage import AgeVerificationPage
from pages.HomePage import HomePage
from pages.LoginPage import LoginPage
import pytest
from constants import (
    ADULT_DATE_OF_BIRTH,
    AUTH_PATH,
    BOTTLE_URL,
    KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
)

def test_valid_age_logged_in_users(driver):
    """Test valid age logged in users."""
    # --- ARRANGE ---
    # Initialize login page and perform authentication
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)

    # Skip the test if the account is currently unavailable (known environment issue)
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)

    # Navigate to the shop section via the homepage
    homepage = HomePage(driver)
    homepage.go_to_shop()

    # --- ACT ---
    # Trigger and handle the mandatory age verification process
    age_verification_modal = AgeVerificationPage(driver)
    age_verification_modal.verify_age(ADULT_DATE_OF_BIRTH)

    # --- ASSERT ---
    # Confirm that age verification was successful
    assert age_verification_modal.is_age_success_displayed()

def _date_18_years_ago() -> date:
    """Date 18 years ago."""
    today = date.today()
    try:
        return today.replace(year=today.year - 18)
    except ValueError:
        # Handles leap-day birthdays in non-leap years.
        return today.replace(month=2, day=28, year=today.year - 18)


def test_user_exactly_18_years_old_today(driver):
    """Test user one day younger than 18."""
    # --- ARRANGE ---
    # Initialize login page and authenticate the test user
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)

    # Skip test if the authentication service is unavailable
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)

    # Proceed to the shop section to trigger the age verification prompt
    homepage = HomePage(driver)
    homepage.go_to_shop()

    # Calculate the birthdate for someone who is exactly 18 years old today
    age_verification_modal = AgeVerificationPage(driver)
    birthdate_18_years_ago = _date_18_years_ago().strftime("%d-%m-%Y")
    age_verification_modal.verify_age(birthdate_18_years_ago)

    # --- ASSERT ---
    # Confirm that the user is successfully verified and granted access
    assert age_verification_modal.is_age_success_displayed()


def test_user_one_day_younger_than_18(driver):
    """Test user one day younger than 18."""
    # --- ARRANGE ---
    # Initialize login page and authenticate the test user
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)

    # Skip the test if the account is currently unavailable (known environment issue
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)

    # Navigate to the shop section to trigger the age verification prompt
    homepage = HomePage(driver)
    homepage.go_to_shop()

    # Calculate a birthdate that makes the user exactly one day too young
    age_verification_modal = AgeVerificationPage(driver)
    birthdate_one_day_too_young = (_date_18_years_ago() + timedelta(days=1)).strftime(
        "%d-%m-%Y"
    )

    # --- ACT ---
    # Submit the underage birthdate in the verification modal
    age_verification_modal.verify_age(birthdate_one_day_too_young)

    # --- ASSERT ---
    # Verify that the system correctly displays the underage alert message
    assert age_verification_modal.is_underage_alert_displayed()


def test_direct_url_bypasses_verification(driver):
    """Test direct url bypasses verification."""
    # --- ARRANGE ---
    # Initialize login page and authenticate the user
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)

    # Skip the test if the account service is currently unavailable
    if AUTH_PATH in driver.current_url and login_page.get_error_displayed():
        pytest.skip(KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON)
    # --- ACT ---
    # Directly navigate to a specific product page (e.g., a bottle of alcohol)
    driver.get(BOTTLE_URL)
    age_verification_modal = AgeVerificationPage(driver)

    # --- ASSERT ---
    # Verify that the age verification modal does NOT appear
    assert age_verification_modal.modal_not_visible()

