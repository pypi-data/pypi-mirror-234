import pytest

from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
confirm request page

@Author: Efrat Cohen
@Date: 03.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Confirm request')]")
CONFIRM_BUTTON = (By.XPATH, "//span[contains(text(),'Confirm')]")


class ConfirmRequestPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_confirm_button(self):
        """
        click on confirm button
        """
        try:
            self.is_element_exist_with_custom_timeout(CONFIRM_BUTTON, pytest.properties.get("timeout") / 10)
            self.click("CONFIRM_BUTTON", CONFIRM_BUTTON)
        except:
            # Close chrome extension popup
            self.driver.close()
            pytest.logger.info("coinbase wallet already connected")
