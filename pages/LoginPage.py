from selenium.webdriver.common.by import By
from pages.BasePage import BasePage


class LoginPage(BasePage):
    # Locators (Write the locators in the form of tuples)
    USERNAME_FIELD_LOCATOR = (By.XPATH, "//input[@type='email']")
    PASSWORD_FIELD_LOCATOR = (By.XPATH, "//input[@type='password']")
    SIGNIN_BUTTON_LOCATOR = (By.XPATH, "//button[@type='submit' and text()='Sign In']")
    ERROR_ALERT_LOCATOR = (By.XPATH, "//div[@role='status']")
    PAGE_URL = 'https://grocerymate.masterschool.com/auth'

    def __init__(self, driver):
        super().__init__(driver)

    def enter_username(self, username):
        self.enter_text(self.USERNAME_FIELD_LOCATOR, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_FIELD_LOCATOR, password)

    def click_login(self):
        self.click(self.SIGNIN_BUTTON_LOCATOR)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()


    def get_error_message(self):
        element = self.find_element(self.ERROR_ALERT_LOCATOR)
        return element.text