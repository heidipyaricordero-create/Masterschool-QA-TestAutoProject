import pytest
from pages.ProductPage import ProductPage
from tests.helper_func import login, open_review_form, PRODUCT_URL, VALID_USER

TEST_USER = VALID_USER
class TestProductPageReviews:
    @pytest.mark.parametrize("char_count,expect_accepted,product_id", [

        (501, False,"66b3a57b3fd5048eacb479a6"),

    ])
    def test_review_character_limit(self, driver, char_count, expect_accepted, product_id):
        login(driver, TEST_USER["email"], TEST_USER["password"])
        page = open_review_form(driver, product_id)
        text = "A" * char_count

        page.select_stars(4)
        page.write_review(text)

        assert page.is_form_error_message_visible()

    @pytest.mark.parametrize("product_id", [

        "66b3a57b3fd5048eacb479a6",

    ])
    def test_submit_review_without_stars_shows_error(self, driver, product_id):
        login(driver, TEST_USER["email"], TEST_USER["password"])
        page = open_review_form(driver, product_id)
        page.write_review("Kein Stern ausgewaehlt.")
        page.submit_review()

        assert page.is_status_error_message_visible()


    @pytest.mark.parametrize("product_id", [

        "66b3a57b3fd5048eacb479a6",

    ])

    def test_review_not_available_for_logged_out_user(self, driver, product_id):
        page = ProductPage(driver)
        page.open(PRODUCT_URL + product_id)


        assert not page.is_submit_btn_visible()







