import pytest
from project.pages.add_customer_page import AddCustomerPage



@pytest.mark.usefixtures("driver")
class TestAddCustomer:

    def test_add_new_customer(self, driver):
        page = AddCustomerPage(driver)
        page.login_admin()                # login as admin
        page.navigate_to_add_customer()   # navigate to Add Customer page
        page.fill_customer_details(
            email="test123@example.com",
            password="test123",
            firstname="Nandyy",
            lastname="Devi",
            gender="Female",
            company="TCS",
            dob="10/23/2000"
        )
        page.save_customer()              # click Save
        assert page.is_customer_added_successfully(), "Customer addition failed!"
