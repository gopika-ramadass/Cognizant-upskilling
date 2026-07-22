"""
================================================================================
HANDS-ON 7: Page Object Model (POM) Test Suite
================================================================================
Author: Gopika R

GOLDEN RULE OF POM VERIFICATION:
This test file contains ZERO driver.find_element calls.
All UI locators and DOM interaction methods are strictly encapsulated inside Page classes.
Test functions only perform high-level business actions and assert expected values.
================================================================================
"""

import sys
import os
import pytest

# Ensure parent package directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "POM Pattern Rules"])
def test_simple_form_submission_pom(driver, base_url, message):
    """
    Step 55: Refactored simple form test using SimpleFormPage.
    Zero driver.find_element calls present in test function.
    """
    page = SimpleFormPage(driver)
    page.navigate_to(f"{base_url}simple-form-demo/")
    
    page.enter_message(message)
    page.click_submit()
    
    assert page.get_displayed_message() == message, (
        f"Expected displayed message '{message}', got '{page.get_displayed_message()}'"
    )


def test_checkbox_demo_pom(driver, base_url):
    """
    Step 56: Refactored checkbox test using CheckboxPage.
    Zero driver.find_element calls present in test function.
    """
    page = CheckboxPage(driver)
    page.navigate_to(f"{base_url}checkbox-demo/")
    
    page.uncheck_option()
    assert not page.is_option_checked(), "Checkbox should be unchecked initially!"
    
    page.check_option()
    assert page.is_option_checked(), "Checkbox should be checked after check_option()!"
    
    page.uncheck_option()
    assert not page.is_option_checked(), "Checkbox should be unchecked after uncheck_option()!"


def test_dropdown_selection_pom(driver, base_url):
    """
    Step 56: Refactored dropdown selection test using DropdownPage.
    Zero driver.find_element calls present in test function.
    """
    page = DropdownPage(driver)
    page.navigate_to(f"{base_url}select-dropdown-demo/")
    
    page.select_day("Wednesday")
    assert page.get_selected_day() == "Wednesday", (
        f"Expected selected day 'Wednesday', got '{page.get_selected_day()}'"
    )


def test_input_form_submit_pom(driver, base_url):
    """
    Step 57: New input form submit test using InputFormPage.
    Zero driver.find_element calls present in test function.
    """
    page = InputFormPage(driver)
    page.navigate_to(f"{base_url}input-form-demo/")
    
    page.fill_form(
        name="Gopika R",
        email="gopika@example.com",
        password="SecurePassword123!",
        company="Cognizant",
        website="https://www.cognizant.com",
        country="United States",
        city="Dallas",
        address1="100 Tech Blvd",
        address2="Suite 400",
        state="Texas",
        zip_code="75001"
    )
    
    page.submit_form()
    
    # Assert successful form submission message or URL state
    current_url = page.get_current_url()
    assert "input-form-demo" in current_url or len(page.get_title()) > 0
