"""
================================================================================
HANDS-ON 7: SimpleFormPage Class
================================================================================
Author: Gopika R
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    """
    Encapsulates all locators and user interactions for the Simple Form Demo page.
    NO ASSERTIONS are performed inside this page class.
    """

    # Class-level locator tuples (Centralized locator management)
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.ID, "showInput")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text: str):
        """Enters specified text into the message input field."""
        input_elem = self.wait_for_element(self.MESSAGE_INPUT)
        input_elem.clear()
        input_elem.send_keys(text)

    def click_submit(self):
        """Clicks the 'Get Checked Value' / Submit button."""
        submit_btn = self.wait_for_clickable(self.SUBMIT_BUTTON)
        submit_btn.click()

    def get_displayed_message(self) -> str:
        """Returns the text displayed in the output message element."""
        output_elem = self.wait_for_element(self.DISPLAYED_MESSAGE)
        return output_elem.text
