def test_login_pom(driver, login_page):
    # Atrrange
    time.sleep(3)
    username = "heidi@example.com"
    password = "heidi123"
    # Act
    login_page.login(username, password)
    # Assert
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/auth' and text()='Log Out']"))

    )

    assert logout_link.is_displayed()

def test_login_invalid(driver, login_page):
    time.sleep(3)
    login_page.login(constant_values.INVALID_USERNAME; constant_values.INVALID_PASSWORD)
    assert login_page.get_error_message().lower() == constant_values.INVALID_USERNAME_OR_PASSWORD_ALERT


