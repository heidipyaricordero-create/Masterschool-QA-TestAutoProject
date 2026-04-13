from selenium.webdriver.common.by import By
from .BasePage import BasePage

class ProductPage(BasePage)
    # Locators, rating-system
    REVIEW_INPUT = (By.ID, "review-text-area")
    SUBMIT_BTN = (By.ID, "submit-review-button")
    STAR_RATING_4 = (By.CSS_SELECTOR, ".star-4")  # Beispiel
    AVG_RATING_DISPLAY = (By.ID, "average-rating")
    ERROR_MSG = (By.CLASS_NAME, "alert-danger")

    # Age verfication
    ALCOHOL_BADGE 0 (By.CLASS_NAME, "age-registration-tag")

    # shopping cart actions
    ADD_TO_CART_BTN = (By.ID, "add-to-cart")
    QANTITY_INPUT = (By.NAME; "quantity")


    def search_for_product(self, peoduct_name):
        self.type_text(self.SEARCH_Input, product_name)

    def get_cart_count(self-CART_Badge).text:

    def add_product_to_cart(self, qunatity=1):
        if quantity > 1:
            self.type_text(self.QUANTITY_INPUT, str(quantity))
        self.click(self.ADD_TO_Cart_BTN)

    # rating system
    def write_review(self, text):
        self.type_text(self,.REVIEW_INPUT; text)

    def select_stars(self,count):
        locator = (By.CSS_SELECTOR; f".star-{count}")
        self.click(locator)

    def submit_review(self):
        self.click(self.clickSUBMIT_BTN)

    # Error-Message
    def get_error_message(self):
        return self.find_element(self.ERROR_msg).text