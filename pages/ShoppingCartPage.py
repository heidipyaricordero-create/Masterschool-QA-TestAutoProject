import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .BasePage import BasePage


class ShoppingCartPage(BasePage):

    CART_ICON = (By.CSS_SELECTOR, ".cart-icon, .fa-shopping-cart")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    CART_TOTAL = (By.CSS_SELECTOR, ".cart-total, .total-price")
    SHIPPING_COST = (By.XPATH, "//*[contains(@class, 'shipping')] | //*[contains(@class, 'delivery')] | //*[contains(text(), 'Shipping')] | //*[contains(text(), 'shipping')]")
    REMOVE_BTN = (By.CSS_SELECTOR, ".remove-item, .cart-item-remove")
    ITEM_QUANTITY_INPUT = (By.CSS_SELECTOR, ".cart-item input[type='number']")
    EMPTY_CART_MSG = (By.CSS_SELECTOR, ".empty-cart, .cart-empty-message")
    ADD_TO_CART_BTN = (By.XPATH, "//div[@class='button-area']//button[contains(@class, 'btn-cart')]")

    def open_cart(self):
        self.click(self.CART_ICON)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CART_ITEMS)
        )

    def get_shipping_cost(self) -> float:
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "*")
            for el in elements:
                try:
                    if el.is_displayed() and any(word in el.text.lower() for word in ["shipping", "delivery", "versand", "kosten"]):
                        return self._parse_price(el.text)
                except:
                    continue
        except:
            pass
        return 0.0

    def get_cart_total(self) -> float:
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "*")
            for el in elements:
                try:
                    if el.is_displayed() and any(word in el.text.lower() for word in ["total", "sum", "gesamt"]):
                        return self._parse_price(el.text)
                except:
                    continue
        except:
            pass
        return 0.0

    def remove_item_by_index(self, index: int = 0):
        remove_btns = self.find_elements(self.REMOVE_BTN)
        remove_btns[index].click()
        WebDriverWait(self.driver, 10).until(
            EC.staleness_of(remove_btns[index])
        )

    def remove_all_items(self):
        while True:
            btns = self.driver.find_elements(*self.REMOVE_BTN)
            if not btns:
                break
            btns[0].click()
            WebDriverWait(self.driver, 10).until(
                EC.staleness_of(btns[0])
            )

    def add_product_to_cart(self, product_url: str, quantity: int = 1):
        self.driver.get(product_url)
        time.sleep(3)

        print(f"Page URL: {self.driver.current_url}")
        print(f"Page Title: {self.driver.title}")

        try:
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print(f"Found {len(all_buttons)} buttons")
            for btn in all_buttons:
                print(f"Button text: '{btn.text}', class: {btn.get_attribute('class')}")
        except:
            pass

        try:
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            print(f"Found {len(all_links)} links")
            for link in all_links[:10]:
                print(f"Link text: '{link.text[:50]}', href: {link.get_attribute('href')}, class: {link.get_attribute('class')}")
        except:
            pass

        try:
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            print(f"Found {len(forms)} forms")
            for form in forms:
                print(f"Form action: {form.get_attribute('action')}, method: {form.get_attribute('method')}")
        except:
            pass

        try:
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            print(f"Found {len(inputs)} inputs")
            for inp in inputs:
                print(f"Input type: {inp.get_attribute('type')}, name: {inp.get_attribute('name')}, id: {inp.get_attribute('id')}")
        except:
            pass

        button_locators = [
            (By.CSS_SELECTOR, "button.btn-cart"),
            (By.CSS_SELECTOR, "button.btn-primary.btn-cart"),
            (By.CSS_SELECTOR, "button.btn.btn-primary"),
            (By.CSS_SELECTOR, "button.btn-primary"),
            (By.CSS_SELECTOR, "button.btn"),
            (By.XPATH, "//button[contains(@class, 'btn-cart')]"),
            (By.XPATH, "//button[contains(@class, 'btn-primary')]"),
        ]

        for locator in button_locators:
            try:
                add_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(locator)
                )
                add_btn.click()
                print(f"Clicked button with locator: {locator}")
                break
            except Exception as e:
                print(f"Failed with {locator}: {e}")
                continue

        time.sleep(3)

    @staticmethod
    def _parse_price(text: str) -> float:
        cleaned = text.replace("€", "").replace(",", ".").strip()
        return float(cleaned)