"""
================================================================================
HANDS-ON 7: Page Object Model — Base Page Class
================================================================================
Author: Gopika R
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    BasePage encapsulates the WebDriver instance and provides common interaction
    methods and explicit wait utilities inherited by all specific page classes.
    """

    def __init__(self, driver):
        self.driver = driver

    def navigate_to(self, url: str):
        """Navigates browser to target URL."""
        self.driver.get(url)

    def get_title(self) -> str:
        """Returns the current page title."""
        return self.driver.title

    def get_current_url(self) -> str:
        """Returns the current browser URL."""
        return self.driver.current_url

    def wait_for_element(self, locator: tuple, timeout: int = 10):
        """Waits for an element identified by (By.<STRATEGY>, 'value') to be visible in DOM."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator: tuple, timeout: int = 10):
        """Waits for an element identified by (By.<STRATEGY>, 'value') to be clickable."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
