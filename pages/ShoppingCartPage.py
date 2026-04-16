# ShoppingCartPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .BasePage import BasePage


class ShoppingCartPage(BasePage):

    # ── Locators ───────────────────────────────────────────────────────────────

    # Warenkorb-Icon / Link
    CART_ICON           = (By.CSS_SELECTOR, ".cart-icon, .fa-shopping-cart")

    # Warenkorb-Seite
    CART_ITEMS          = (By.CSS_SELECTOR, ".cart-item")
    CART_TOTAL          = (By.CSS_SELECTOR, ".cart-total, .total-price")
    SHIPPING_COST       = (By.CSS_SELECTOR, ".shipping-cost, .delivery-cost")

    # Artikel entfernen
    REMOVE_BTN          = (By.CSS_SELECTOR, ".remove-item, .cart-item-remove")

    # Quantity pro Artikel
    ITEM_QUANTITY_INPUT = (By.CSS_SELECTOR, ".cart-item input[type='number']")

    # Leerer Warenkorb
    EMPTY_CART_MSG      = (By.CSS_SELECTOR, ".empty-cart, .cart-empty-message")


    # ── Methoden ───────────────────────────────────────────────────────────────

    def open_cart(self):
        self.click(self.CART_ICON)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CART_ITEMS)
        )

    def get_shipping_cost(self) -> float:
        """Liest den Versandkostenbetrag aus und gibt ihn als float zurück."""
        text = self.find_element(self.SHIPPING_COST).text
        return self._parse_price(text)

    def get_cart_total(self) -> float:
        """Liest den Gesamtbetrag aus und gibt ihn als float zurück."""
        text = self.find_element(self.CART_TOTAL).text
        return self._parse_price(text)

    def remove_item_by_index(self, index: int = 0):
        """Entfernt einen Artikel per Index (0 = erster Artikel)."""
        remove_btns = self.find_elements(self.REMOVE_BTN)
        remove_btns[index].click()
        WebDriverWait(self.driver, 10).until(
            EC.staleness_of(remove_btns[index])
        )

    def remove_all_items(self):
        """Entfernt alle Artikel aus dem Warenkorb."""
        while True:
            btns = self.driver.find_elements(*self.REMOVE_BTN)
            if not btns:
                break
            btns[0].click()
            WebDriverWait(self.driver, 10).until(
                EC.staleness_of(btns[0])
            )

    def add_product_to_cart(self, product_url: str, quantity: int = 1):
        """Navigiert zu einem Produkt und legt es in den Warenkorb."""
        self.driver.get(product_url)
        wait = WebDriverWait(self.driver, 10)

        if quantity > 1:
            qty_input = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "quantity"))
            )
            qty_input.clear()
            qty_input.send_keys(str(quantity))

        add_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-cart"))
        )
        add_btn.click()

    # ── Hilfsmethode ───────────────────────────────────────────────────────────

    @staticmethod
    def _parse_price(text: str) -> float:
        """Wandelt z.B. '4,99 €' oder '€4.99' in float 4.99 um."""
        cleaned = text.replace("€", "").replace(",", ".").strip()
        return float(cleaned)