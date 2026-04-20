"""Centralized constants shared by page objects and tests."""

BASE_URL = "https://grocerymate.masterschool.com"
AUTH_PATH = "/auth"

AUTH_URL = f"{BASE_URL}{AUTH_PATH}"
STORE_URL = f"{BASE_URL}/store"
CART_URL = f"{BASE_URL}/cart"
CELERY_PRODUCT_URL = f"{BASE_URL}/product/66b3a57b3fd5048eacb47a9b"

TEST_USER_EMAIL = "johndoe@example.com"
TEST_USER_PASSWORD = "admin123"
TEST_USER = {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}

KNOWN_ACCOUNT_UNAVAILABLE_SKIP_REASON = (
    "Known test account is unavailable in current environment."
)

ADULT_DATE_OF_BIRTH = "01-01-1990"
