from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    EMAIL_FIELD = (By.ID, "Email")
    PASSWORD_FIELD = (By.ID, "Password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.login-button")
    LOGOUT_BUTTON = (By.XPATH, "//a[text()='Logout']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ✅ Add this function
    def open_login_page(self):
        self.driver.get("https://admin-demo.nopcommerce.com/login")

    def login(self, email="admin@yourstore.com", password="admin"):
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD)).clear()
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)
        self.driver.find_element(*self.PASSWORD_FIELD).clear()
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        self.wait.until(EC.title_contains("Dashboard"))

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_BUTTON))

    def is_logged_in(self):
        return "Dashboard" in self.driver.title

    def is_logged_out(self):
        return "Login" in self.driver.title
