import pytest
from pages.ProductPage import ProductPage
from tests.helper_func import login, open_review_form, PRODUCT_URL, VALID_USER

TEST_USER = VALID_USER


class TestProductPageReviews:
    @pytest.mark.parametrize(
        "char_count,expect_accepted,product_id",
        [
            (501, False, "66b3a57b3fd5048eacb479a6"),
        ],
    )
    def test_review_character_limit(self, driver, char_count, expect_accepted, product_id):
        """Test review character limit."""
        # --- ARRANGE ---
        # Log in as a registered user
        login(driver, TEST_USER["email"], TEST_USER["password"])

        # Navigate to the product review form
        page = open_review_form(driver, product_id)

        # Generate a string of a specific length to test character limit
        text = "A" * char_count
        # --- ACT ---
        # Fill in the review with a 4-star rating and the generated text
        page.select_stars(4)
        page.write_review(text)

        # --- ASSERT ---
        # Verify that an error message is shown
        assert page.is_form_error_message_visible()

    @pytest.mark.parametrize(
        "product_id",
        [
            "66b3a57b3fd5048eacb479a6",
        ],
    )
    def test_submit_review_without_stars_shows_error(self, driver, product_id):
        """Test submit review without stars shows error."""
        # --- ARRANGE ---
        # Log in as a registered user
        login(driver, TEST_USER["email"], TEST_USER["password"])

        # Navigate to the product review form
        page = open_review_form(driver, product_id)

        # write review, without stars chosen and submit
        page.write_review("Kein Stern ausgewaehlt.")
        page.submit_review()

        # --- ASSERT ---
        # Verify that an error message is shown
        assert page.is_status_error_message_visible()




    @pytest.mark.parametrize(
        "product_id",
        [
            "66b3a57b3fd5048eacb479a6",
        ],
    )
    def test_review_not_available_for_logged_out_user(self, driver, product_id):
        """Test review not available for logged out user."""
        # Navigate to the product
        page = ProductPage(driver)
        page.open(PRODUCT_URL + product_id)

        # --- ASSERT ---
        # Verify that an error message is shown
        assert not page.is_submit_btn_visible()







