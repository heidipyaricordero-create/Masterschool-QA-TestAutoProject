import pytest
import math
from pages.ProductPage import ProductPage
from pages.ShoppingCartPage import ShoppingCartPage
from selenium.webdriver.common.keys import Keys
from tests.helper_func import login, open_review_form, PRODUCT_URL, VALID_USER

VALID_USER = {
    "email": "johndoe@example.com",
    "password": "admin123"
}


class TestShoppingCart:

    @pytest.mark.parametrize("cart_value, expected_free_shipping", [
        (19.99, False),
        (20.00, True),
        (500.00, True),
    ])


    def test_shipping_cost_threshold(self, driver, cart_value, expected_free_shipping):
        login(driver, VALID_USER["email"], VALID_USER["password"])
        shopping_cart_page = ShoppingCartPage(driver)

        shopping_cart_page.open_cart()
        shopping_cart_page.remove_all_items()
        shopping_cart_page.navigate().open_first_product().add_to_cart()
        shopping_cart_page.open_cart()

        single_item_price = shopping_cart_page.get_cart_total()

        needed_quantity = math.ceil(cart_value / single_item_price)

        shopping_cart_page.set_item_quantity(needed_quantity)
        actual_total = shopping_cart_page.get_cart_total()
        shipping_cost = shopping_cart_page.get_shipping_cost()

        print(f"Warenwert: {actual_total}, Versandkosten: {shipping_cost}")

        if expected_free_shipping:
            assert shipping_cost == 0.0, f"Fehler: Versand sollte kostenlos sein bei {actual_total}€"
        else:
            assert shipping_cost > 0.0, f"Fehler: Versandkosten sollten anfallen bei {actual_total}€"









    # def test_shipping_recalculated_after_removing_items(self, driver, logged_in, cleared_cart):
    #     product_page = ProductPage(driver)
    #     cart_page = ShoppingCartPage(driver)
    #     cart_page.navigate()
    #     cart_page.open_first_product()
    #     try:
    #         product_page.set_quantity_and_add_to_cart(80)
    #     except Exception:
    #         pytest.skip("Could not add product to cart in current app state.")
    #
    #     cart_page.open_cart()
    #     try:
    #         assert cart_page.get_shipping_cost() == pytest.approx(0.0, abs=0.01)
    #     except Exception:
    #         pytest.skip("Shipping element is unavailable in current app state.")
    #
    #     while cart_page.get_cart_total() > 19.99:
    #         cart_page.remove_item_by_index(0)
    #
    #     assert cart_page.get_shipping_cost() > 0.00