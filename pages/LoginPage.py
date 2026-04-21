from selenium.webdriver.common.by import By
from pages.BasePage import BasePage
from constants import AUTH_URL


class LoginPage(BasePage):

    URL = AUTH_URL
    EMAIL_FIELD = (By.CSS_SELECTOR, "input[type='email'], input#email")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password'], input#password")
    SIGNIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    LOGOUT_BTN = (By.XPATH, "//button[contains(@class, 'logout-btn')] | //a[contains(., 'Log Out')]")
    ERROR_ALERT = (
        By.XPATH,
        "//div[@role='status' and contains(., 'Invalid username or password')] | //div[contains(@class, 'alert')]",
    )

    def __init__(self, driver):
        super().__init__(driver)

    def load(self):
        return self.open(self.URL)

    def enter_email(self, email):
        self.type_text(self.EMAIL_FIELD, email)
        return self

    def enter_password(self, password):
        self.type_text(self.PASSWORD_FIELD, password)
        return self

    def click_signin(self):
        self.click(self.SIGNIN_BTN)
        return self

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_signin()
        return self

    def logout_displayed(self):
        return self.is_visible(self.LOGOUT_BTN)

    def get_error_displayed(self):
        return self.is_visible(self.ERROR_ALERT)
