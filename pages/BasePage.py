from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
        Parent class for all page objects.

        Provides shared browser interaction helpers so individual
        page objects can focus purely on page-specific behavior
    """

    DEFAULT_TIMEOUT = 30

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)
        # -- Navigation --

    def open(self, url):
        self.driver.get(url)
        return self

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def find(self, locator):
        """Wait for and return a single element"""
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator):
        """Return all matching elements (legacy alias)."""
        return self.find_all(locator)

    def find_all(self, locator):
        """Return all matching elements"""
        self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )
        return self.driver.find_elements(*locator)

    def is_visible(self, locator, timeout=5):
        """Return True if element is visible within timeout"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def click(self, locator):
        """Wait for element to be clickable, then click it"""
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def type_text(self, locator, text):
        """Clear field and type text."""
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Return visible text of an element"""
        return self.find(locator).text.strip()

    def get_attribute(self, locator, attribute):
        """Get the value of a specified attribute from a web element"""
        return self.find(locator).get_attribute(attribute)

    def scroll_to(self, locator):
        """Find the element and scroll it into view"""
        element = self.find(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", element
        )

    def wait_for_url(self, partial_url, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(partial_url)
        )

    def wait_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def screenshot(self, name="screenshot"):
        self.driver.save_screenshot(f"{name}.png")



