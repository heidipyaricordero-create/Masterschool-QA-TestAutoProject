from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from .BasePage import BasePage
import time
from selenium.webdriver.common.keys import Keys
from constants import (
    CART_URL as APP_CART_URL,
    STORE_URL as APP_STORE_URL,
)


class ShoppingCartPage(BasePage):

    STORE_URL = APP_STORE_URL
    CART_URL = APP_CART_URL
    CART_ICON = (By.XPATH, "//div[@class='headerIcon'][3]")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    CART_TOTAL = (By.XPATH, "//div[@class='total-container']/h5[2]")
    SHIPPING_COST = (By.XPATH, "//div[@class='shipment-container']/h5[2]")
    REMOVE_BTN = (By.CSS_SELECTOR, ".remove-item, .cart-item-remove")
    EMPTY_CART_MSG = (By.CSS_SELECTOR, ".empty-cart, .cart-empty-message, .cart-empty")
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".cart-item-quantity, input[name='quantity']")
    ADD_TO_CART_BTN = (By.XPATH, "//div[@class='button-area']//button[contains(@class, 'btn-cart')]")
    PRODUCT_LINK = (By.CSS_SELECTOR, "a[href*='/store/product/']")
    REMOVE_ICON = (By.XPATH, "//a[@class='remove-icon']")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-card")
    NEXT_PAGE_BUTTON = (By.XPATH, "//button[@class='pagination-link' and contains(text(),'Next')]")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate(self):
        self.open(self.STORE_URL)
        return self


    def open_cart(self):

        self.click(self.CART_ICON)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-summary, h2"))
        )

        return self
    def find_product(self, product_name):

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card"))
        )

        cards = self.driver.find_elements(By.CSS_SELECTOR, ".card")

        for card in cards:
            try:
                title_element = card.find_element(By.CSS_SELECTOR, ".lead")

                current_name = title_element.text.strip().lower()
                target_name = product_name.strip().lower()

                if target_name in current_name:

                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                    return card
            except NoSuchElementException:
                continue

        raise Exception(f"Produkt '{product_name}' wurde nicht gefunden! Gefundene Karten: {len(cards)}")

    def add_product(self, product_name, quantity=1):

        card = self.find_product(product_name)
        add_button = card.find_element(By.CSS_SELECTOR, ".btn-cart")
        quantity_input = card.find_element(By.CSS_SELECTOR, ".quantity")
        if int(quantity) > 1:
            quantity_input.clear()
            quantity_input.send_keys(quantity)
        add_button.click()


        import time
        time.sleep(2)




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


        target_input.send_keys(Keys.ENTER)

        self.wait_visible(self.CART_TOTAL)
        return self

    def get_shipping_cost(self) -> float:
        element = self.wait_visible(self.SHIPPING_COST, timeout=10)
        return self._parse_price(element.text)

    def get_cart_total(self):
        try:
            # Warte, bis das Summen-Element sichtbar ist
            element = self.wait_visible(self.CART_TOTAL, timeout=10)

            return float(element.text.replace('€', '').replace('Total:', '').strip())
        except TimeoutException:
            # Falls es nicht erscheint, ist der Warenkorb evtl. leer
            print("DEBUG: CART_TOTAL nicht gefunden. Ist der Warenkorb leer?")
            return 0.0

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

    def decrease_quantity(self, product, decrease_factor):
        minus_button_xpath = f"//h5[text()='{product}']/ancestor::div[contains(@class,'flex-grow-1')]//button[@class='minus']"
        minus_button = self.driver.find_element(By.XPATH, minus_button_xpath)
        for i in range(decrease_factor):
            minus_button.click()

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


