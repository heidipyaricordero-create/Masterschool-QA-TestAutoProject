from selenium.webdriver.common.by import By
from pages.BasePage import BasePage

class AgeVerificationPage(BasePage):
    DOB_INPUT = (By.XPATH, "//input[@type='text' and @placeholder='DD-MM-YYYY']")
    CONFIRM_BTN = (By.XPATH, "//div[@class='modal-content'/button[text()='Confirm']")
    UNDERAGE_ALERT = (By.XPATH, "//div[@role='status' and contains(text(), 'You are underage')]")
    AGE_SUCCESS_ALERT = (By.XPATH, "//div[@role='status' and contains(text(), 'You are of age')]")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_dob(self, dob):
        """dob format: DD-MM-YYYY
        """
        self.type_text(self.DOB_INPUT, dob)
        return self

    def click_confirm(self):
        self.click(self.CONFIRM_BTN)
        return self

    def verify_age(self, dob):
        self.enter_dob(dob)
        self.click_confirm()
        return self

    def is_underage_alert_displayed(self):
        return self.is_visible(self.UNDERAGE_ALERT)

    def is_age_success_displayed(self):
        return self.is_visible(self.AGE_SUCCESS_ALERT)


