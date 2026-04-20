import pytest
from pages.ShoppingCartPage import ShoppingCartPage
from pages.ProductPage import ProductPage
from pages.ShoppingCartPage import ShoppingCartPage


class TestShoppingCart:


    @pytest.mark.parametrize("cart_value, expected_free_shipping", [
        (19.99, False),
        (20.00, True),
        (500.00, True),
    ])


    def test_shipping_cost_threshold(self, driver, logged_in, cleared_cart, cart_value, expected_free_shipping):
        # 1. Page Objects lokal instanziieren

        product_page = ProductPage(driver)
        shopping_cart_page = ShoppingCartPage(driver)
        product_price = 0.70

        # 2. Vorbereitung
        quantity = round(cart_value / product_price)

        # 3. Ablauf
        shopping_cart_page.navigate()
        shopping_cart_page.handle_modal()
        shopping_cart_page.open_first_product()

        shopping_cart_page.handle_modal()
        product_page.set_quantity_and_add_to_cart(quantity)

        # 4. Validierung
        shopping_cart_page.navigate()
        shipping = shopping_cart_page.get_shipping_cost()

        if expected_free_shipping:
            assert shipping == 0.00, f"Fehler: Bei {cart_value}€ sollte Versand kostenlos sein!"
        else:
            assert shipping > 0.00, f"Fehler: Bei {cart_value}€ sollten Versandkosten anfallen!"

    def test_shipping_recalculated_after_removing_items(self, driver, logged_in, cleared_cart):
        #  Objekte lokal erstellen

        product_page = ProductPage(driver)
        cart_page = ShoppingCartPage(driver)

        # 1. Warenkorb füllen
        shopping_cart_page.navigate()
        store_page.handle_modal()
        store_page.open_first_product()
        product_page.set_quantity_and_add_to_cart(80)

        cart_page.navigate()
        assert cart_page.get_shipping_cost() == 0.00

        # 2. Artikel entfernen
        while cart_page.get_cart_total() > 15.00:
            cart_page.remove_item_by_index(0)

        # 3. Finale Prüfung
        assert cart_page.get_shipping_cost() > 0.00