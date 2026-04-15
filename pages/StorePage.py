from selenium.webdriver.common. by import By
from pages.BasePage import BasePage

class StorePage(BasePage):

    AGE_FIELD_LOCATOR = (By.XPATH, "//input[@type='text' and @placeholder='DD-MM-YYYY']")

    def __init__(self,driver):
        super().__init__(driver)

