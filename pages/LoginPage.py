from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class LoginPage(BasePage):

    URL = "https://grocerymate.masterschool.com/auth"
    EMAIL_FIELD = (By.XPATH, "//input[@type='email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@type='password']")
    SIGNIN_BTN = (By.XPATH, "//button[@type='submit' and text()='Sign In']")
    LOGOUT_BTN = (By.XPATH, "//button[@class='logout-btn']")
    ERROR_ALERT = (By.XPATH, "//div[@role='status' and text()='Invalid username or password']")

    # ---Actions---
    def __init__(self, driver):
        super().__init__(driver)

    def load(self):
        return self.open(self. URL)

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

    def logout_displayed(self):
        return self.is_visible(self.LOGOUT_BTN)

    def get_error_displayed(self):
        return self.is_visible(self.ERROR_ALERT)
