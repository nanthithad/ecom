from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .login_page import LoginPage


class AddCustomerPage:
    # Locators
    CUSTOMERS_MENU = (By.XPATH, "//a[@href='#']//p[contains(text(),'Customers')]")
    CUSTOMERS_ITEM = (By.XPATH, "//a[@href='/Admin/Customer/List']//p[contains(text(),'Customers')]")
    ADD_NEW_BUTTON = (By.CSS_SELECTOR, "a.btn-primary")
    GENERAL_TAB = (By.XPATH, "//a[@href='#general']")  # Make General tab active
    EMAIL_FIELD = (By.ID, "Email")
    PASSWORD_FIELD = (By.ID, "Password")
    FIRSTNAME_FIELD = (By.ID, "FirstName")
    LASTNAME_FIELD = (By.ID, "LastName")
    GENDER_MALE = (By.ID, "Gender_Male")
    GENDER_FEMALE = (By.ID, "Gender_Female")
    DOB_FIELD = (By.ID, "DateOfBirth")
    COMPANY_FIELD = (By.ID, "Company")
    SAVE_BUTTON = (By.NAME, "save")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.login_page = LoginPage(driver)

    def login_admin(self):
        self.login_page.open_login_page()
        self.login_page.login(email="admin@yourstore.com", password="admin")

    def navigate_to_add_customer(self):
        self.wait.until(EC.element_to_be_clickable(self.CUSTOMERS_MENU)).click()
        self.wait.until(EC.element_to_be_clickable(self.CUSTOMERS_ITEM)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_NEW_BUTTON)).click()

    def fill_customer_details(self, email, password, firstname, lastname, gender, company, dob):
        """Fill the Add Customer form with waits, without assuming a tab exists"""

        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD)).send_keys(email)
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*self.FIRSTNAME_FIELD).send_keys(firstname)
        self.driver.find_element(*self.LASTNAME_FIELD).send_keys(lastname)

        if gender.lower() == "male":
            self.driver.find_element(*self.GENDER_MALE).click()
        else:
            self.driver.find_element(*self.GENDER_FEMALE).click()

        # Wait for DOB field to be visible
        try:
            self.wait.until(EC.visibility_of_element_located(self.DOB_FIELD)).send_keys(dob)
        except TimeoutException:
            print("DOB field not visible, skipping DOB input.")

        # Wait for Company field to be visible
        try:
            self.wait.until(EC.visibility_of_element_located(self.COMPANY_FIELD)).send_keys(company)
        except TimeoutException:
            print("Company field not visible, skipping Company input.")

        # Scroll Save button into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            self.driver.find_element(*self.SAVE_BUTTON)
        )

    def save_customer(self):
        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON)).click()

    def is_customer_added_successfully(self):
        success_text = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_ALERT)).text
        return "The new customer has been added successfully." in success_text
