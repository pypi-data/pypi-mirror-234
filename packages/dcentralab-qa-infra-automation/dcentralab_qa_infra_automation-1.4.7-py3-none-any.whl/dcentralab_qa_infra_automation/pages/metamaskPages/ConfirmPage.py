from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
confirm metamask wallet page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
CONFIRM_BUTTON = (By.XPATH, "//*[contains(text(),'Confirm')]")


class ConfirmPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("CONFIRM_BUTTON", CONFIRM_BUTTON)

    def is_confirm_button_exist(self):
        """
        check is confirm button exist
        """
        return self.is_element_exist("CONFIRM_BUTTON", CONFIRM_BUTTON)

    def click_on_confirm_button(self):
        """
        click on confirm button
        """
        self.click("CONFIRM_BUTTON", CONFIRM_BUTTON)
