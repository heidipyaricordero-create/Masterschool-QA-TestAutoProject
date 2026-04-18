import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.ShoppingCartPage import ShoppingCartPage

CART_URL    = "https://grocerymate.masterschool.com/cart"
PRODUCT_URL = "https://grocerymate.masterschool.com/store/product/celery"
PRODUCT_URL = 0.70
VALID_USER  = {"email": "test@example.com", "password": "Test1234!"}

class TestShoppingCart:

@pytest.fixture(autouse=True)
def setup(self, driver):
    self.driver = driver
    self.page = ShoppingCartPage(driver)

@pytest.mark.parametrize("cart_value,expected_free_shipping", [
    (19.99, False),
    (20.00, True),
    (500.00, True),
    ])

def test_shipping_free_at_exact_threshold(self, driver, logged_in, cleared_cart):
    page = ShoppingCartPage(driver)
    quantity = round(19.99 / 0.70)
    page.add_product_to_cart("celery", quantity)

    shipping = page.get_shipping_cost()
    assert shipping == 0.00

def test_shipping_charged_below_threshold(self, driver, logged_in, cleared_cart):
    page = ShoppingCartPage(driver)
    quantity = round(19.99 / 0.70)

    shipping = page.get_shipping_cost()
    assert shipping > 0.00


def test_shipping_free_for_high_value_cart(self, driver, logged_in, cleared_cart):
    page = ShoppingCartPage(driver)
    quantity = round(500.00 / 0.70)
    page.add_product_to_cart("celery", quantity)

    shipping = page.get_shipping_cost()
    assert shipping == 0.00

def test_shipping_recalculated_after_removing_items(self, driver,logged_in, cleared_cart):
    page = ShoppingCartPage(driver)
    quantity = round(55.00 / 0.70)
    page.add_product_to_cart("celery", quantity)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".shipping-cost"))
    )

    shipping_before = page.get_cart_total()
    while total > 15.00:
        page.remove_item_by_index(0)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total"))

        )

        total = page.geet_cart_total()

        shipping_after = page.get_shipping_cost()
        assert shipping_after > 0.00





