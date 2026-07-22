"""
================================================================================
HANDS-ON 7: InputFormPage Class
================================================================================
Author: Gopika R
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InputFormPage(BasePage):
    """
    Encapsulates all locators and form interaction methods for the Input Form Submit page.
    """

    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "inputEmail4")
    PASSWORD_INPUT = (By.ID, "inputPassword4")
    COMPANY_INPUT = (By.ID, "company")
    WEBSITE_INPUT = (By.ID, "websitename")
    COUNTRY_SELECT = (By.NAME, "country")
    CITY_INPUT = (By.ID, "inputCity")
    ADDRESS1_INPUT = (By.ID, "inputAddress1")
    ADDRESS2_INPUT = (By.ID, "inputAddress2")
    STATE_INPUT = (By.ID, "inputState")
    ZIP_INPUT = (By.ID, "inputZip")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Submit')]")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-msg")

    def fill_form(
        self,
        name: str,
        email: str,
        password: str,
        company: str,
        website: str,
        country: str,
        city: str,
        address1: str,
        address2: str,
        state: str,
        zip_code: str,
    ):
        """Fills out all fields on the Input Form Submit page."""
        self.wait_for_element(self.NAME_INPUT).send_keys(name)
        self.wait_for_element(self.EMAIL_INPUT).send_keys(email)
        self.wait_for_element(self.PASSWORD_INPUT).send_keys(password)
        self.wait_for_element(self.COMPANY_INPUT).send_keys(company)
        self.wait_for_element(self.WEBSITE_INPUT).send_keys(website)

        # Select Country dropdown
        country_elem = self.wait_for_element(self.COUNTRY_SELECT)
        select_country = Select(country_elem)
        try:
            select_country.select_by_visible_text(country)
        except Exception:
            select_country.select_by_value("US")

        self.wait_for_element(self.CITY_INPUT).send_keys(city)
        self.wait_for_element(self.ADDRESS1_INPUT).send_keys(address1)
        self.wait_for_element(self.ADDRESS2_INPUT).send_keys(address2)
        self.wait_for_element(self.STATE_INPUT).send_keys(state)
        self.wait_for_element(self.ZIP_INPUT).send_keys(zip_code)

    def submit_form(self):
        """Clicks the form Submit button."""
        submit_btn = self.wait_for_clickable(self.SUBMIT_BUTTON)
        submit_btn.click()

    def get_success_message(self) -> str:
        """Returns the success confirmation message after form submission."""
        success_elem = self.wait_for_element(self.SUCCESS_MESSAGE)
        return success_elem.text
