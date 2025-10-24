import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Update this path to your downloaded chromedriver.exe
CHROMEDRIVER_PATH = r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe"

@pytest.fixture(scope="class")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Uncomment for headless mode:
    # options.add_argument("--headless")

    # Use your manually downloaded chromedriver
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(10)
    request.cls.driver = driver

    yield driver
    driver.quit()
