"""
================================================================================
HANDS-ON 6 & 7: Pytest Shared Fixtures & Configuration Hooks
================================================================================
Author: Gopika R
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Step 48: Session-scoped fixture for base_url
@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


# Step 41: Function-scoped driver fixture with setup (yield) and teardown (quit)
@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    _driver = webdriver.Chrome(service=service, options=options)
    _driver.set_window_size(1280, 800)
    _driver.implicitly_wait(5)
    
    yield _driver
    
    _driver.quit()


# Step 46: Pytest hook to capture a screenshot on test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture:
            test_name = item.name.replace("[", "_").replace("]", "_").replace("-", "_")
            screenshot_filename = f"{test_name}_failure.png"
            try:
                driver_fixture.save_screenshot(screenshot_filename)
                print(f"\n[HOOK] Screenshot captured on test failure: {screenshot_filename}")
            except Exception as e:
                print(f"\n[HOOK] Failed to capture screenshot on failure: {e}")
