from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class CategoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Navigation
        self.catalog_menu = (By.XPATH, "//a[@href='#']//p[contains(text(),'Catalog')]")
        self.categories_menu = (By.XPATH, "//a[@href='/Admin/Category/List']//p[contains(text(),'Categories')]")

        # Category actions
        self.add_new_button = (By.XPATH, "//a[@class='btn btn-primary']")
        self.category_name_field = (By.ID, "Name")
        self.save_button = (By.NAME, "save")
        self.success_message = (By.XPATH, "//div[@class='alert alert-success alert-dismissable']")

    def navigate_to_categories(self):
        self.wait.until(EC.element_to_be_clickable(self.catalog_menu)).click()
        self.wait.until(EC.element_to_be_clickable(self.categories_menu)).click()

    def add_category(self, name):
        self.wait.until(EC.element_to_be_clickable(self.add_new_button)).click()
        self.wait.until(EC.visibility_of_element_located(self.category_name_field)).send_keys(name)
        self.driver.find_element(*self.save_button).click()

    def edit_category(self, old_name, new_name):
        # Find the edit button corresponding to the category
        edit_button = self.driver.find_element(By.XPATH, f"//td[text()='{old_name}']/following-sibling::td/a[contains(text(),'Edit')]")
        edit_button.click()
        name_field = self.driver.find_element(*self.category_name_field)
        name_field.clear()
        name_field.send_keys(new_name)
        self.driver.find_element(*self.save_button).click()


    def is_success_message_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.success_message)).is_displayed()
