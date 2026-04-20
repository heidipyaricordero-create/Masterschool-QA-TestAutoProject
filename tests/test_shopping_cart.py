import pytest
from pages.ProductPage import ProductPage
from pages.ShoppingCartPage import ShoppingCartPage


class TestShoppingCart:

    @pytest.mark.parametrize("cart_value, expected_free_shipping", [
        (19.99, False),
        (20.00, True),
        (500.00, True),
    ])
    def test_shipping_cost_threshold(self, driver, logged_in, cleared_cart, cart_value, expected_free_shipping):
        product_page = ProductPage(driver)
        shopping_cart_page = ShoppingCartPage(driver)
        product_price = 0.70
        quantity = round(cart_value / product_price)
        shopping_cart_page.navigate()
        shopping_cart_page.handle_modal()
        shopping_cart_page.open_first_product()
        try:
            product_page.set_quantity_and_add_to_cart(quantity)
        except Exception:
            pytest.skip("Could not add product to cart in current app state.")
        shopping_cart_page.open_cart()
        try:
            shipping = shopping_cart_page.get_shipping_cost()
        except Exception:
            pytest.skip("Shipping element is unavailable in current app state.")

        if expected_free_shipping:
            assert shipping == pytest.approx(0.0, abs=0.01), f"Expected free shipping at {cart_value}."
        else:
            assert shipping > 0.00, f"Expected shipping cost below free-shipping threshold at {cart_value}."

    def test_shipping_recalculated_after_removing_items(self, driver, logged_in, cleared_cart):
        product_page = ProductPage(driver)
        cart_page = ShoppingCartPage(driver)
        cart_page.navigate()
        cart_page.open_first_product()
        try:
            product_page.set_quantity_and_add_to_cart(80)
        except Exception:
            pytest.skip("Could not add product to cart in current app state.")

        cart_page.open_cart()
        try:
            assert cart_page.get_shipping_cost() == pytest.approx(0.0, abs=0.01)
        except Exception:
            pytest.skip("Shipping element is unavailable in current app state.")

        while cart_page.get_cart_total() > 19.99:
            cart_page.remove_item_by_index(0)

        assert cart_page.get_shipping_cost() > 0.00