import pytest
from project.pages.login_page import LoginPage
from project.pages.category_page import CategoryPage

@pytest.mark.usefixtures("driver")
class TestCategoryManagement:

    def test_category_crud(self, driver):
        driver.get("https://admin-demo.nopcommerce.com/login")

        # Login
        login_page = LoginPage(driver)
        login_page.login("admin@yourstore.com", "admin")

        # Navigate to categories
        category_page = CategoryPage(driver)
        category_page.navigate_to_categories()

        # Add category
        category_page.add_category("Test Category 123")
        assert category_page.is_success_message_displayed(), "Category addition failed"

        # Edit category
        category_page.edit_category("Test Category 123", "Updated Category 123")
        assert category_page.is_success_message_displayed(), "Category edit failed"


