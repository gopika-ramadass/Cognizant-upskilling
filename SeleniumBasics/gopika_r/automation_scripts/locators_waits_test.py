"""
================================================================================
HANDS-ON 5: Locators — ID, Name, XPath, CSS Selectors & Explicit Waits
================================================================================
Author: Gopika R

LOCATOR STRATEGY PREFERENCE RANKING & MAINTAINABILITY JUSTIFICATION:

Rank 1: By.ID
- Why: Fastest execution, uniquely identifies elements (DOM specification requires unique IDs),
  and is resilient to UI layout and structural HTML changes.

Rank 2: By.NAME
- Why: High uniqueness in form inputs, clean readability, independent of CSS layout styling.

Rank 3: By.CSS_SELECTOR
- Why: Faster execution engine than XPath in modern browsers, clean concise syntax, supports
  pseudo-classes and complex parent-child/attribute matching.

Rank 4: By.XPATH (Relative with Attributes - e.g. //input[@id='val'])
- Why: Flexible, supports bidirectional DOM traversal (parent/ancestor axes) and text matching
  (text(), contains()), but slightly slower execution than CSS selectors.

Rank 5: By.CLASS_NAME
- Why: Often non-unique (classes are shared across multiple elements for styling), susceptible to
  CSS framework refactoring.

Rank 6: By.XPATH (Absolute Path - e.g. /html/body/div[1]/div/section[2]/div/div/div[1]/div[1]/div[2]/form/div/input)
- Why: WORST locator strategy. Extremely fragile — breaks on any DOM structural change, div insertion,
  or layout update. Never use absolute XPaths in production test suites!
================================================================================
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager


def get_headless_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1280, 800)
    return driver


def test_task1_locators():
    print("\n--- Task 1: Locator Strategies (Simple to Robust) ---")
    driver = get_headless_driver()
    try:
        url = "https://www.lambdatest.com/selenium-playground/simple-form-demo"
        driver.get(url)

        # Step 32: Locate input element using 6 different locator strategies
        print("Testing 6 Locator Strategies on Simple Form Demo message input:")
        
        # 1. By.ID
        elem_id = driver.find_element(By.ID, "user-message")
        print("  1. By.ID -> Found tag:", elem_id.tag_name, "| id:", elem_id.get_attribute("id"))

        # 2. By.NAME (Searching input with placeholder attribute)
        elem_name = driver.find_element(By.XPATH, "//input[@placeholder='Please enter your Message']")
        print("  2. By.NAME / Attr -> Found tag:", elem_name.tag_name)

        # 3. By.CLASS_NAME
        elem_class = driver.find_element(By.CLASS_NAME, "form-control")
        print("  3. By.CLASS_NAME -> Found tag:", elem_class.tag_name)

        # 4. By.TAG_NAME
        elem_tag = driver.find_element(By.TAG_NAME, "input")
        print("  4. By.TAG_NAME -> Found tag:", elem_tag.tag_name)

        # 5. By.XPATH (Structural ancestor path)
        elem_xpath_abs = driver.find_element(By.XPATH, "//div//input[@id='user-message']")
        print("  5. By.XPATH (Structural Ancestor) -> Found tag:", elem_xpath_abs.tag_name)

        # 6. By.XPATH (Relative path with attributes)
        elem_xpath_rel = driver.find_element(By.XPATH, "//input[@id='user-message']")
        print("  6. By.XPATH (Relative Attribute) -> Found tag:", elem_xpath_rel.tag_name)

        # Step 33: 3 Different CSS Selectors for the same element
        print("\nTesting 3 CSS Selector Variations for the same element:")
        # Variation A: By ID (#id)
        css_1 = driver.find_element(By.CSS_SELECTOR, "#user-message")
        # Variation B: By Attribute ([id='value'])
        css_2 = driver.find_element(By.CSS_SELECTOR, "input[id='user-message']")
        # Variation C: By Parent-Child relationship (div > input)
        css_3 = driver.find_element(By.CSS_SELECTOR, "div > input#user-message")
        
        assert css_1.get_attribute("id") == "user-message", "CSS Selector 1 failed!"
        assert css_2.get_attribute("id") == "user-message", "CSS Selector 2 failed!"
        assert css_3.get_attribute("id") == "user-message", "CSS Selector 3 failed!"
        print("  ASSERTION PASSED: All 3 CSS Selectors successfully located the target element.")

        # Step 34: Checkbox Demo XPath with text() and contains()
        print("\nTesting Checkbox Demo XPath text() and contains():")
        driver.get("https://www.lambdatest.com/selenium-playground/checkbox-demo")
        
        # XPath with text() / contains text
        label_option1 = driver.find_element(By.XPATH, "//label[contains(text(),'Option 1')]")
        print("  Found label via XPath text():", label_option1.text)
        assert "Option 1" in label_option1.text, "XPath text() lookup failed!"

        # XPath with contains()
        all_option_labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
        print(f"  Found {len(all_option_labels)} option labels via XPath contains().")
        assert len(all_option_labels) >= 1, "XPath contains() failed to find option labels!"

        print("--- Task 1 Completed Successfully ---")
    finally:
        driver.quit()


def test_task2_waits():
    print("\n--- Task 2: WebDriverWait, Explicit Waits & FluentWait ---")
    driver = get_headless_driver()
    try:
        url = "https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo"
        driver.get(url)

        # Step 36: Bootstrap Alerts demo - Click Success Message button & wait for alert
        print("1. Triggering Success Message alert and waiting with WebDriverWait...")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        btn_success = None
        for b in buttons:
            if "success" in b.text.lower():
                btn_success = b
                break
        if not btn_success:
            btn_success = buttons[0]
        
        print(f"   Found target button: '{btn_success.text.strip()}'")
        btn_success.click()

        # Step 36: Explicit wait for visibility of element located
        wait = WebDriverWait(driver, 10)
        alert_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@class,'alert') or contains(text(),'Success') or contains(text(),'autocloseable')]")))
        alert_text = alert_element.text
        print(f"   Alert Text Captured: '{alert_text.strip()}'")
        assert len(alert_text) > 0, "Alert text assertion failed!"
        print("   ASSERTION PASSED: Alert appeared and contains expected text.")

        # Step 37: Performance comparison - time.sleep(3) vs Explicit Wait
        print("\n2. Timing Comparison: time.sleep(3) vs Explicit Wait:")
        
        # Method A: time.sleep(3)
        start_sleep = time.time()
        btn_success.click()
        time.sleep(3)
        alert_sleep = driver.find_element(By.XPATH, "//*[contains(@class,'alert')]")
        time_sleep_dur = time.time() - start_sleep
        print(f"   Fixed time.sleep(3) duration: {time_sleep_dur:.3f} seconds")

        # Method B: Explicit Wait
        start_explicit = time.time()
        btn_success.click()
        alert_explicit = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(@class,'alert')]"))
        )
        time_explicit_dur = time.time() - start_explicit
        print(f"   Explicit Wait duration: {time_explicit_dur:.3f} seconds")
        print(f"   Explicit Wait was {time_sleep_dur - time_explicit_dur:.3f} seconds FASTER!")

        # Step 38: Element clickable wait & explanation
        # ============================================================================
        # EXPLICIT WAIT COMPARISON EXPLANATION:
        # 1. EC.visibility_of_element_located: Checks that an element is present in DOM,
        #    is displayed (display != none), and has height/width > 0.
        # 2. EC.element_to_be_clickable: Checks visibility AND verifies that the element
        #    is enabled (is_enabled() == True) and NOT obscured by any modal/spinner overlay.
        #    Always use element_to_be_clickable before calling .click() to avoid
        #    ElementClickInterceptedException.
        # ============================================================================
        print("\n3. Waiting for button to be clickable via EC.element_to_be_clickable...")
        clickable_btn = wait.until(EC.element_to_be_clickable(btn_success))
        clickable_btn.click()
        print("   Successfully clicked button after element_to_be_clickable wait.")

        # Step 39: FluentWait implementation with 500ms polling ignoring NoSuchElementException
        print("\n4. Demonstrating FluentWait with 500ms polling frequency:")
        fluent_wait = WebDriverWait(
            driver,
            timeout=10,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException, ElementNotInteractableException]
        )
        normal_alert = fluent_wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(@class,'alert')]"))
        )
        print(f"   FluentWait successfully resolved element text: '{normal_alert.text.strip()}'")
        assert len(normal_alert.text) > 0, "FluentWait assertion failed!"

        print("--- Task 2 Completed Successfully ---")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_task1_locators()
    test_task2_waits()
