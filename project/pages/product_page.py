from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Navigation
        self.catalog_menu = (By.XPATH, "//a[@href='#']//p[contains(text(),'Catalog')]")
        self.products_menu = (By.XPATH, "//a[@href='/Admin/Product/List']//p[contains(text(),'Products')]")

        # Product actions
        self.add_new_button = (By.XPATH, "//a[@class='btn btn-primary']")
        self.product_name_field = (By.ID, "Name")
        self.product_price_field = (By.ID, "Price")
        self.save_button = (By.NAME, "save")
        self.success_message = (By.XPATH, "//div[@class='alert alert-success alert-dismissable']")

    def navigate_to_products(self):
        self.wait.until(EC.element_to_be_clickable(self.catalog_menu)).click()
        self.wait.until(EC.element_to_be_clickable(self.products_menu)).click()

    def add_product(self, name, price):
        self.wait.until(EC.element_to_be_clickable(self.add_new_button)).click()
        self.wait.until(EC.visibility_of_element_located(self.product_name_field)).send_keys(name)
        self.driver.find_element(*self.product_price_field).send_keys(price)
        self.driver.find_element(*self.save_button).click()

    def is_success_message_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.success_message)).is_displayed()
