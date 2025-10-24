import os
import tempfile
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Existing Windows ChromeDriver path
WINDOWS_CHROMEDRIVER_PATH = r"C:\chromedriver-win64\chromedriver-win64\chromedriver.exe"


@pytest.fixture(scope="class")
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    if os.environ.get("GITHUB_ACTIONS") == "true":
        # Headless + CI tweaks
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        # Create unique temp user-data-dir
        temp_user_data_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={temp_user_data_dir}")

        # Use webdriver-manager for GitHub Actions
        service = Service(ChromeDriverManager().install())
    else:
        # Local Windows path
        service = Service(WINDOWS_CHROMEDRIVER_PATH)

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    request.cls.driver = driver
    yield driver
    driver.quit()
