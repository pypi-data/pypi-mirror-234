from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
receive crypto to your username page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Receive crypto to your username')]")
DENY_BUTTON = (By.XPATH, "//*[contains(text(),'Deny')]")


class ReceiveCryptoToUsernamePage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_deny(self):
        self.click("DENY_BUTTON", DENY_BUTTON)
