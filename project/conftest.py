import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

# Update this path for local dev only; GitHub Actions will use installed chromedriver
CHROMEDRIVER_PATH = r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe"


@pytest.fixture(scope="class")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Headless mode for CI (GitHub Actions)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

    # Use local chromedriver for local dev
    if os.environ.get("GITHUB_ACTIONS") == "true":
        driver = webdriver.Chrome(options=options)
    else:
        from selenium.webdriver.chrome.service import Service
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(10)
    request.cls.driver = driver

    yield driver
    driver.quit()
