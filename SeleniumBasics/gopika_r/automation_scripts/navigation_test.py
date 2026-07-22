"""
================================================================================
HANDS-ON 4 - TASK 2: WebDriver Navigation and Window Commands
================================================================================
Author: Gopika R
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def run_navigation_test():
    print("--- Starting Task 2: WebDriver Navigation and Window Commands ---")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.implicitly_wait(10)
        base_url = "https://www.lambdatest.com/selenium-playground/"

        # Step 28: Navigate to Selenium Playground
        print(f"1. Opening base URL: {base_url}")
        driver.get(base_url)

        # Navigate to Simple Form Demo page by clicking link
        print("2. Clicking 'Simple Form Demo' link...")
        simple_form_link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
        simple_form_link.click()

        # Assert URL contains 'simple-form-demo'
        current_url = driver.current_url
        print(f"   Current URL: {current_url}")
        assert "simple-form-demo" in current_url, f"Expected 'simple-form-demo' in URL, got {current_url}"
        print("   ASSERTION PASSED: URL contains 'simple-form-demo'")

        # Navigate back using driver.back()
        print("3. Navigating back to main playground using driver.back()...")
        driver.back()
        assert "simple-form-demo" not in driver.current_url, "Failed to navigate back!"
        print("   Navigated back successfully.")

        # Step 29: Open new browser tab using window.open
        print("4. Opening a new tab with https://www.google.com via execute_script...")
        driver.execute_script('window.open("https://www.google.com");')

        # List all window handles
        handles = driver.window_handles
        print(f"   Total window handles open: {len(handles)}")
        assert len(handles) == 2, "Expected 2 window handles to be open!"

        # Switch to the new tab (index 1)
        print("5. Switching to new tab (Google tab)...")
        driver.switch_to.window(handles[1])
        google_title = driver.title
        print(f"   Google Tab Title: '{google_title}'")
        assert "Google" in google_title or len(google_title) > 0, "Failed to fetch Google tab title!"

        # Step 30: Switch back to original tab (index 0) and capture screenshot
        print("6. Switching back to original tab (Playground tab)...")
        driver.switch_to.window(handles[0])

        screenshot_path = "playground_screenshot.png"
        driver.save_screenshot(screenshot_path)
        assert os.path.exists(screenshot_path), "Screenshot file was not created!"
        print(f"   ASSERTION PASSED: Screenshot successfully saved to '{screenshot_path}'.")

        # Step 31: Demonstrate get_window_size() and set_window_size(1280, 800)
        # ============================================================================
        # WHY CONSISTENT WINDOW SIZE MATTERS FOR RESPONSIVE UI AUTOMATION:
        # Modern web applications use CSS media queries and responsive layouts (flexbox/grid)
        # that break, hide, or alter elements at different viewport resolutions (e.g. collapsing
        # navigation bars into hamburger menus on mobile/tablet viewports).
        # Setting an explicit, consistent window size (e.g. 1280x800) ensures tests run
        # deterministically across local developer machines, headful browsers, and CI build nodes,
        # preventing false test failures caused by hidden elements or viewport wrapping.
        # ============================================================================
        initial_size = driver.get_window_size()
        print(f"7. Initial Window Size: {initial_size}")

        driver.set_window_size(1280, 800)
        new_size = driver.get_window_size()
        print(f"   Updated Window Size: {new_size}")
        assert new_size["width"] == 1280 and new_size["height"] == 800, "Window size update failed!"
        print("   ASSERTION PASSED: Window size successfully set to 1280x800.")

        print("--- Task 2 Navigation Test Completed Successfully ---")

    finally:
        driver.quit()


if __name__ == "__main__":
    run_navigation_test()
