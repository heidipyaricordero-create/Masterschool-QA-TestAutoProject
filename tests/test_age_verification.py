from pages.AgeVerificationPage import AgeVerificationPage
from pages.HomePage import HomePage
from pages.LoginPage import LoginPage
from datetime import date, timedelta

def test_valid_age_logged_in_users(driver):
    # Step 1 Login
    login_page = LoginPage(driver)
    login_page.load()
    # Step 2: Homepage
    homepage = login_page.login("johndoe@examole.com", "admin123")
    homepage.go_to_shop()
    # Step 3 Age Verification
    age_verification_modal = AgeVerificationPage(driver)
    age_verification_modal.verify_age("01-01-1990")

    assert age_verification_modal.is_age_success_displayed()

def test_user_exactly_18_years_old_today(driver):
    login_page = LoginPage(driver)
    login_page.load()
    homepage = login_page.login("johndoe@example.com", "admin123")
    homepage.go_to_shop()

    age_verification_modal.verify_age(birthdate_18_years_ago)

    assert age_verification_modal.is_age_sucess_displayed()


def test_user_one_day_younger_than18(driver):
    login_page = LoginPage(driver)
    login_page.load()
    homepage = login_page.login("johndoe@example.com", "admin123")
    homepage.go_to_shop

    age_verification_modal = AgeVerificationPage(driver)
    tomorrow = date.today() + timedelta(days=1)
    birthdate = tomorrow.replace(year=tomorrow.year - 18)
    birthdate_str = birthdate.strftime("%d-%m-%Y")

    assert age_verification_modal.is_underage_alert_displayed()


def test_direct_url_bypasses_verification(driver):
    login_page = LoginPage(driver)
    login_page.load()