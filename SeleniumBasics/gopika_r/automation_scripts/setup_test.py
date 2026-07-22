"""
================================================================================
HANDS-ON 4 - TASK 1: Selenium Architecture and Environment Setup
================================================================================
Author: Gopika R

SELENIUM COMPONENT ARCHITECTURE OVERVIEW:

1. Selenium WebDriver:
   - What it is: A web automation framework that directly controls native browser
     engines (Chrome, Firefox, Edge, Safari) without requiring an intermediate script.
   - Communication Mechanism: Operates using W3C WebDriver standard HTTP RESTful APIs
     (JSON Wire Protocol legacy / W3C WebDriver spec standard). Commands sent from 
     client language bindings (Python) pass through browser-specific drivers (ChromeDriver)
     to directly manipulate browser DOM nodes and emulate real user actions.

2. Selenium Grid:
   - What problem it solves: Solves cross-browser, multi-platform scalability issues
     by enabling parallel execution of test suites across multiple remote machines,
     virtual environments, docker containers, and operating systems (Windows, Linux, macOS).
   - Architecture: Consists of a Hub (central router) that distributes test execution
     requests across connected Nodes (machines running specific OS/browser versions).

3. Selenium IDE:
   - What it is: A browser extension (available for Chrome & Firefox) providing record-and-playback
     capabilities for rapid prototyping of simple automation scripts.
   - Use Cases: Used for quick exploratory testing, creating bug reproduction steps,
     and auto-generating baseline test code skeletons in target languages (Python, Java).
================================================================================
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def run_setup_test():
    print("--- Starting Task 1: Selenium Architecture & Environment Setup ---")

    # Configure Chrome Options for Headless Execution
    options = Options()
    # Step 27: Modify script to run in headless mode using ChromeOptions
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Step 25: Initialize Chrome WebDriver using webdriver-manager
    print("Downloading/locating ChromeDriver via webdriver-manager...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Step 26: Add implicit wait
        # ============================================================================
        # IMPLICIT WAIT GLOBAL BAD PRACTICE EXPLANATION:
        # Setting driver.implicitly_wait(10) globally tells WebDriver to poll the DOM
        # for up to 10 seconds for ANY element lookup throughout the entire session.
        # WHY THIS IS BAD PRACTICE:
        # 1. Increases Execution Time on Negative Tests: When asserting element absence,
        #    the test is forced to wait the full 10s timeout before throwing NoSuchElement.
        # 2. Unpredictable Interactions with Explicit Waits: Combining implicit and explicit
        #    waits leads to non-deterministic wait times (e.g., 10s implicit + 10s explicit = 20s delay).
        # 3. DOM State Insufficiency: Implicit wait ONLY checks element presence in DOM,
        #    NOT visibility, clickability, or animation completion. Explicit waits must be preferred.
        # ============================================================================
        driver.implicitly_wait(10)

        # Step 25: Navigate to LambdaTest Selenium Playground
        target_url = "https://www.lambdatest.com/selenium-playground/"
        print(f"Navigating to: {target_url}")
        driver.get(target_url)

        # Step 25 & 27: Print page title and verify headless execution success
        page_title = driver.title
        print(f"Successfully retrieved page title in Headless Mode: '{page_title}'")
        assert "Selenium Grid Online" in page_title or "LambdaTest" in page_title, "Page title verification failed!"
        print("ASSERTION PASSED: Page title verified successfully in Headless mode.")

    finally:
        # Step 25: Close browser
        print("Closing browser driver session...")
        driver.quit()
        print("--- Task 1 Setup Test Completed Successfully ---\n")


if __name__ == "__main__":
    run_setup_test()
