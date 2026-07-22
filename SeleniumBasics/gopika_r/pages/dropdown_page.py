"""
================================================================================
HANDS-ON 7: DropdownPage Class
================================================================================
Author: Gopika R
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class DropdownPage(BasePage):
    """
    Encapsulates locators and interactions for the Select Dropdown List page.
    Uses Selenium's Select helper class internally.
    """

    SELECT_DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name: str):
        """Selects a day option from the select dropdown list by value/text."""
        dropdown_element = self.wait_for_element(self.SELECT_DROPDOWN)
        select_obj = Select(dropdown_element)
        select_obj.select_by_value(day_name)

    def get_selected_day(self) -> str:
        """Returns the text of the currently selected option."""
        dropdown_element = self.wait_for_element(self.SELECT_DROPDOWN)
        select_obj = Select(dropdown_element)
        return select_obj.first_selected_option.text
