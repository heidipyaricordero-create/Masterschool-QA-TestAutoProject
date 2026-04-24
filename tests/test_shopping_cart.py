import pytest
from constants import ADULT_DATE_OF_BIRTH
from pages.AgeVerificationPage import AgeVerificationPage
from pages.ShoppingCartPage import ShoppingCartPage
from tests.helper_func import login, VALID_USER


class TestShoppingCart:


    @pytest.mark.parametrize("product_name, quantity, cart_value, expected_free_shipping", [
        ("Galia Melon", 2, 3.6, False),
        ("Gala Apples", 50, 100, True),
    ])
    def test_shipping_cost_threshold(self, driver, product_name, quantity, cart_value, expected_free_shipping):

        login(driver, VALID_USER["email"], VALID_USER["password"])

        shopping_cart_page = ShoppingCartPage(driver)

        shopping_cart_page.open_cart()

        shopping_cart_page.remove_all_items()

        shopping_cart_page.navigate()

        age_verification_modal = AgeVerificationPage(driver)

        age_verification_modal.verify_age(ADULT_DATE_OF_BIRTH)

        # Find the product and add to cart, with given quantity

        shopping_cart_page.add_product(product_name, quantity)

        shopping_cart_page.open_cart()

        actual_total = shopping_cart_page.get_cart_total()

        shipping_cost = shopping_cart_page.get_shipping_cost()

        print(f"Warenwert: {actual_total}, Versandkosten: {shipping_cost}")

        if expected_free_shipping:

            assert shipping_cost == 0.0, f"Fehler: Versand sollte kostenlos sein bei {actual_total}€"

        else:

            assert shipping_cost > 0.0, f"Fehler: Versandkosten sollten anfallen bei {actual_total}€"


    @pytest.mark.parametrize("product_name, initial_quantity, decrease_factor, expected_free_shipping", [
        ("Gala Apples", 10, 3, False),
    ])
    @pytest.mark.xfail(reason='Known Bug: Shipping threshold logic does not work correctly')
    def test_shipping_recalculated_after_removing_items(self, driver, product_name, initial_quantity, decrease_factor, expected_free_shipping):
        login(driver, VALID_USER["email"], VALID_USER["password"])
        shopping_cart_page = ShoppingCartPage(driver)

        shopping_cart_page.open_cart()
        shopping_cart_page.remove_all_items()
        shopping_cart_page.navigate()
        age_verification_modal = AgeVerificationPage(driver)
        age_verification_modal.verify_age(ADULT_DATE_OF_BIRTH)
        # Find the product and add to cart, with given quantity
        shopping_cart_page.add_product(product_name, initial_quantity)
        shopping_cart_page.open_cart()

        # Decrease quantity
        shopping_cart_page.decrease_quantity(product_name, decrease_factor)
        shipping_cost = shopping_cart_page.get_shipping_cost()

        if expected_free_shipping:
            assert shipping_cost == 0.0
        else:
            assert shipping_cost > 0.0




