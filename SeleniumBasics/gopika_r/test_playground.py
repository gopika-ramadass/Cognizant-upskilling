"""
================================================================================
HANDS-ON 6: Running Selenium Tests with pytest
================================================================================
Author: Gopika R
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Step 42 & 45: Parameterised form submission test with 3 different input values
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):
    """
    Step 42 & 45: Opens Simple Form Demo, enters input message, clicks submit,
    and asserts displayed text equals the parameterized message input.
    """
    target_url = f"{base_url}simple-form-demo/"
    driver.get(target_url)

    # Locate input field and enter message
    user_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-message"))
    )
    user_input.clear()
    user_input.send_keys(message)

    # Click Submit / Get Checked Value button
    show_btn = driver.find_element(By.ID, "showInput")
    show_btn.click()

    # Wait for output element and assert text
    display_elem = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert display_elem.text == message, f"Expected message '{message}', but got '{display_elem.text}'"


def test_checkbox_demo(driver, base_url):
    """
    Step 43: Opens Checkbox Demo, clicks first checkbox, asserts selected state,
    clicks again and asserts deselected state.
    """
    target_url = f"{base_url}checkbox-demo/"
    driver.get(target_url)

    # Locate first checkbox on the page
    checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))
    )

    # Ensure unselected state initially
    if checkbox.is_selected():
        checkbox.click()
    assert not checkbox.is_selected(), "Checkbox should initially be unchecked!"

    # Click to check
    driver.execute_script("arguments[0].click();", checkbox)
    assert checkbox.is_selected(), "Checkbox should be selected after click!"

    # Click to uncheck
    driver.execute_script("arguments[0].click();", checkbox)
    assert not checkbox.is_selected(), "Checkbox should be deselected after second click!"


def test_dropdown_selection(driver, base_url):
    """
    Step 49: Opens Select Dropdown List demo, uses Select helper class to choose
    'Wednesday', and asserts selected option text is 'Wednesday'.
    """
    target_url = f"{base_url}select-dropdown-demo/"
    driver.get(target_url)

    # Locate select dropdown
    dropdown_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "select-demo"))
    )
    select_obj = Select(dropdown_element)

    # Choose 'Wednesday'
    select_obj.select_by_value("Wednesday")

    # Assert selected option text
    selected_option = select_obj.first_selected_option
    assert selected_option.text == "Wednesday", f"Expected 'Wednesday', but got '{selected_option.text}'"
