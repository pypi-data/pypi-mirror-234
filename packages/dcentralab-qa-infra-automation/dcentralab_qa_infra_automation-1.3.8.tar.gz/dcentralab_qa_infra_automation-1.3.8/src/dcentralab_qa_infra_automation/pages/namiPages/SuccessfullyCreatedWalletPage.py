from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
successfully created wallet page

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(), 'Successfully')]")
CLOSE_BTN = (By.XPATH, "//button[contains(text(), 'Close')]")


class SuccessfullyCreatedWalletPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_close_button(self):
        """
        click on close button
        """
        self.click("CLOSE_BTN", CLOSE_BTN)