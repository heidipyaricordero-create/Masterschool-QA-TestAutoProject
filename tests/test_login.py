from pages.LoginPage import LoginPage
from pages.HomePage import HomePage

def test_login(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login("johndoe@example.com", "admin123")
    homepage = HomePage(driver)
    assert homepage.is_logout_displayed()


