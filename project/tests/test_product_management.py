import pytest
from project.pages.login_page import LoginPage
from project.pages.product_page import ProductPage

@pytest.mark.usefixtures("driver")
class TestProductManagement:

    def test_add_product(self, driver):
        driver.get("https://admin-demo.nopcommerce.com/login")

        # Login
        login_page = LoginPage(driver)
        login_page.login("admin@yourstore.com", "admin")

        # Navigate and add product
        product_page = ProductPage(driver)
        product_page.navigate_to_products()
        product_page.add_product("Test Product 123", "99.99")

        # Assertion
        assert product_page.is_success_message_displayed(), "Product addition failed"
