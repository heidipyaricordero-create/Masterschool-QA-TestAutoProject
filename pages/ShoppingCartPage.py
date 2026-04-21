from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .BasePage import BasePage
from constants import (
    CART_URL as APP_CART_URL,
    CELERY_PRODUCT_URL as APP_CELERY_PRODUCT_URL,
    STORE_URL as APP_STORE_URL,
)


class ShoppingCartPage(BasePage):
    STORE_URL = APP_STORE_URL
    CART_URL = APP_CART_URL
    DEFAULT_PRODUCT_URL = APP_CELERY_PRODUCT_URL
    CART_ICON = (By.CSS_SELECTOR, ".cart-icon, .fa-shopping-cart")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    CART_TOTAL = (By.XPATH, "//*[contains(translate(., 'TOTALSUMGESAMT', 'totalsumgesamt'), 'total') or contains(translate(., 'TOTALSUMGESAMT', 'totalsumgesamt'), 'sum') or contains(translate(., 'TOTALSUMGESAMT', 'totalsumgesamt'), 'gesamt')]")
    SHIPPING_COST = (By.XPATH, "//*[contains(translate(., 'SHIPPINGDELIVERYVERSAND', 'shippingdeliveryversand'), 'shipping') or contains(translate(., 'SHIPPINGDELIVERYVERSAND', 'shippingdeliveryversand'), 'delivery') or contains(translate(., 'SHIPPINGDELIVERYVERSAND', 'shippingdeliveryversand'), 'versand')]")
    REMOVE_BTN = (By.CSS_SELECTOR, ".remove-item, .cart-item-remove")
    EMPTY_CART_MSG = (By.CSS_SELECTOR, ".empty-cart, .cart-empty-message, .cart-empty")
    ADD_TO_CART_BTN = (By.XPATH, "//div[@class='button-area']//button[contains(@class, 'btn-cart')]")
    PRODUCT_LINK = (By.CSS_SELECTOR, "a[href*='/store/product/']")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate(self):
        self.open(self.STORE_URL)
        return self

    def open_cart(self):
        self.open(self.CART_URL)
        return self

    def handle_modal(self):
        # Placeholder for compatibility with existing tests.
        return self

    def open_first_product(self):
        links = self.driver.find_elements(*self.PRODUCT_LINK)
        if links:
            links[0].click()
        else:
            self.open(self.DEFAULT_PRODUCT_URL)
        return self

    def get_shipping_cost(self) -> float:
        element = self.wait_visible(self.SHIPPING_COST, timeout=10)
        return self._parse_price(element.text)

    def get_cart_total(self) -> float:
        element = self.wait_visible(self.CART_TOTAL, timeout=10)
        return self._parse_price(element.text)

    def remove_item_by_index(self, index: int = 0):
        remove_btns = self.find_elements(self.REMOVE_BTN)
        if index >= len(remove_btns):
            raise IndexError("Remove button index out of range")
        target = remove_btns[index]
        target.click()
        self.wait.until(EC.staleness_of(target))

    def remove_all_items(self):
        while True:
            btns = self.driver.find_elements(*self.REMOVE_BTN)
            if not btns:
                break
            target = btns[0]
            target.click()
            self.wait.until(EC.staleness_of(target))

    @staticmethod
    def _parse_price(text: str) -> float:
        cleaned = (
            text.replace("€", "")
            .replace(",", ".")
            .replace("Shipping", "")
            .replace("Total", "")
            .strip()
        )
        parts = [p for p in cleaned.split() if p]
        for part in reversed(parts):
            try:
                return float(part)
            except ValueError:
                continue
        raise ValueError(f"Could not parse price from: {text}")