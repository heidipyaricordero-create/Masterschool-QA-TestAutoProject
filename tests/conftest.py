import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pages.LoginPage import LoginPage
from pages.ShoppingCartPage import ShoppingCartPage

# Konstanten (Tipp: Pfade am besten relativ oder in einer config halten)
CHROMEDRIVER_PATH = r"C:\Users\akass\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
CART_URL = "https://grocerymate.masterschool.com/cart"


@pytest.fixture(scope="function")
def driver():
    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = Options()
    options.add_argument("--start-maximized")
    # Falls der Browser im Hintergrund laufen soll: options.add_argument("--headless")

    driver = webdriver.Chrome(service=service, options=options)
    driver.delete_all_cookies()

    # Implicit Wait ist okay, aber wir verlassen uns primär auf Explicit Waits in den Pages
    driver.implicitly_wait(5)

    yield driver
    driver.quit()


@pytest.fixture()
def logged_in(driver):
    """Loggt den User ein, indem die LoginPage genutzt wird (Strenges POM)."""
    login_page = LoginPage(driver)
    login_page.driver.get("https://grocerymate.masterschool.com/auth")

    # Nutze die Methoden deiner LoginPage statt find_element hier!
    login_page.login("johndoe@example.com", "admin123")

    # Optional: Warte hier kurz, bis ein Element der Startseite sichtbar ist
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "user-profile")))

    return driver


@pytest.fixture()
def cleared_cart(driver, logged_in):
    """Stellt sicher, dass der Warenkorb vor dem Test leer ist."""
    cart_page = ShoppingCartPage(driver)
    # Nutze eine Methode in der ShoppingCartPage, um zum Warenkorb zu navigieren
    driver.get(CART_URL)
    cart_page.remove_all_items()
    return driver