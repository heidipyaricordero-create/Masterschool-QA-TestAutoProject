from selenium.webdriver.common.by import By
from.BasePage import BasePage

class HomePage(BasePage):
    SHOP_LINK = (By.XPATH, "//ul[@class='anim-nav']//a[@href='/store']")
    ACCOUNT_ICON = (By.XPATH, "(//*[@class='headerIcon'])[1]")
    CART_ICON = (By.XPATH, "(//*[@class='headerIcon'])[3]")
    LOGOUT_LINK = (By.XPATH, "//a[@href='/auth' and text()='Log Out']")

    def __init__(self, driver):
        super().__init__(driver)


    def navigate_to_home(self):
        self.driver.get("https://grocerymate.masterschool.com")


    def click_shop(self):
        self.click(self.SHOP_LINK)

    def click_account(self):
        self.click(self.ACCOUNT_ICON)
        return self

    def open_cart(self):
        self.click(self.CART_ICON)
        return self

    def go_to_shop(self):
        self.click(self.SHOP_LINK)


    def logout_displayed(self):
        # check, if logout.link is visible
        try:
            return self.find_element(self.LOGOUT_LINK).is_displayed()
        except:
            return False





