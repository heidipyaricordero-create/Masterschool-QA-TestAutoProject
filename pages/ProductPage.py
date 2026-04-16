from selenium.webdriver.common.by import By
from .BasePage import BasePage

class ProductPage(BasePage):

    # Shopping Cart
    ADD_TO_CART_BTN        = (By.CSS_SELECTOR, ".btn-cart")
    QUANTITY_INPUT         = (By.CLASS_NAME, "quantity")

    # Age Verification
    AGE_VERIFICATION_MODAL = (By.CLASS_NAME, "modal-overlay")
    BIRTHDATE_INPUT        = (By.XPATH, "//input[@placeholder='DD-MM-YYYY']")
    CONFIRM_BTN            = (By.XPATH, "//button[text()='Confirm']")

    # Review / Rating
    STAR_RATING            = (By.CSS_SELECTOR, "span.star")        # alle Sterne
    REVIEW_INPUT           = (By.CSS_SELECTOR, "textarea.new-review-form-control")
    SUBMIT_BTN             = (By.CSS_SELECTOR, ".new-review-btn-send")
    CANCEL_BTN             = (By.CSS_SELECTOR, ".new-review-btn-cancel")


    def add_product_to_cart(self, quantity=1):
        if quantity > 1:
            self.type_text(self.QUANTITY_INPUT, str(quantity))
        self.click(self.ADD_TO_CART_BTN)

    def confirm_age_verification(self, birthdate):
        self.type_text(self.BIRTHDATE_INPUT, birthdate)
        self.click(self.CONFIRM_BTN)

    def select_stars(self, count):
        # click stars (1-5)
        stars = self.find_elements(self.STAR_RATING)
        stars[count - 1].click()

    def write_review(self, text):
        self.type_text(self.REVIEW_INPUT, text)

    def submit_review(self):
        self.click(self.SUBMIT_BTN)

    def cancel_review(self):
        self.click(self.CANCEL_BTN)