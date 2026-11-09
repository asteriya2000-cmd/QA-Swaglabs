import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"


@pytest.fixture
def driver():
    options = Options()
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,768")
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


@pytest.fixture
def inventory_page(driver):
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    page = InventoryPage(driver)
    page.title()
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        if browser:
            SCREENSHOTS_DIR.mkdir(exist_ok=True)
            file_name = item.name.replace("/", "_").replace("[", "_").replace("]", "")
            browser.save_screenshot(str(SCREENSHOTS_DIR / f"{file_name}.png"))
