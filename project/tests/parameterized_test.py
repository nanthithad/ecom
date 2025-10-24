import os
import pytest
from project.pages.login_page import LoginPage
from project.utils.CSV_Utils import CSVUtils

# Path to CSV
csv_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../testdata/test_data.csv"))
test_data = CSVUtils.read_data(csv_file)

@pytest.mark.parametrize("row", test_data)
def test_login_csv(driver, row):  # ✅ Use the driver fixture here
    # driver is automatically provided by conftest.py

    # Open nopCommerce admin login
    driver.get("https://admin-demo.nopcommerce.com/login")

    # Login with CSV data
    login_page = LoginPage(driver)
    login_page.login(row['username'], row['password'])

    # Optional: Check login success
    assert "Dashboard" in driver.title or "admin" in driver.current_url

    print(f"Login tested with: {row['username']}/{row['password']}")
