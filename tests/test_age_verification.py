from pages.AgeVerificationPage import AgeVerificationPage
from pages.HomePage import HomePage
from pages.LoginPage import LoginPage


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
