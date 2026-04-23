from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .BasePage import BasePage
from selenium.webdriver.common.keys import Keys
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
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".cart-item-quantity, input[name='quantity']")
    ADD_TO_CART_BTN = (By.XPATH, "//div[@class='button-area']//button[contains(@class, 'btn-cart')]")
    PRODUCT_LINK = (By.CSS_SELECTOR, "a[href*='/store/product/']")
    REMOVE_ICON = (By.XPATH, "a[@class='remove-icon']")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate(self):
        self.open(self.STORE_URL)
        return self

    def open_cart(self):
        self.open(self.CART_URL)
        return self

    def add_to_cart(self, wait_for_success=True):

        button = self.wait_visible(self.ADD_TO_CART_BTN)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)

        button.click()

        if wait_for_success:
            self.wait.until(EC.element_to_be_clickable(self.CART_ICON))

        return self

    def handle_modal(self):
        # Placeholder for compatibility with existing tests.
        return self

    def set_item_quantity(self, quantity: int, index: int = 0):
        inputs = self.find_elements(self.QUANTITY_INPUT)
        if index >= len(inputs):
            raise IndexError("Quantity input index out of range")

        target_input = inputs[index]
        target_input.clear()
        target_input.send_keys(str(quantity))

        # Oft muss man Enter drücken oder aus dem Feld tabben, um den Preis zu aktualisieren
        target_input.send_keys(Keys.ENTER)

        # Kurz warten, bis sich der Total-Preis aktualisiert hat (Staleness oder Preis-Check)
        self.wait_visible(self.CART_TOTAL)
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

            links = self.driver.find_elements(*self.REMOVE_ICON)
            if not links:
                break

            target = links[0]
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