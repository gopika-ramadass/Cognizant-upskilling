"""
================================================================================
HANDS-ON 7: CheckboxPage Class
================================================================================
Author: Gopika R
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CheckboxPage(BasePage):
    """
    Encapsulates locators and interactions for the Checkbox Demo page.
    Uses JavaScript clicks to handle custom/styled checkboxes robustly.
    """

    # Targets the first checkbox input on the demo page
    FIRST_CHECKBOX = (By.XPATH, "(//input[@type='checkbox'])[1]")

    def _get_checkbox(self):
        """Returns the first checkbox element after waiting for presence."""
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.FIRST_CHECKBOX)
        )

    def check_option(self):
        """Ensures the checkbox is checked, using JS click for reliability."""
        checkbox = self._get_checkbox()
        if not checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)

    def uncheck_option(self):
        """Ensures the checkbox is unchecked, using JS click for reliability."""
        checkbox = self._get_checkbox()
        if checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)

    def is_option_checked(self) -> bool:
        """Returns True if the first checkbox is selected, False otherwise."""
        return self._get_checkbox().is_selected()
