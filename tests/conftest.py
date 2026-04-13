import pytest
from selenium import webdriver

@pytest.fixture(scope='functoin')
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver

    driver.quit()