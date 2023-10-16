from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
connect wallet popup

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//div[contains(@class, 'css-djq4ow')]")
ACCEPT_BTN = (By.XPATH, "//button[contains(text(), 'Access')]")


class ConnectWalletPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("ACCEPT_BTN", ACCEPT_BTN)

    def click_on_accept_button(self):
        """
        click on accept button
        """
        self.click("ACCEPT_BTN", ACCEPT_BTN)