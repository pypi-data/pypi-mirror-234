from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
metamask install completed page

@Author: Efrat Cohen
@Date: 07.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Your MetaMask install is complete!')]")
NEXT_BUTTON = (By.XPATH, "//*[contains(text(),'Next')]")
DONE_BUTTON = (By.XPATH, "//*[contains(text(),'Done')]")
TRY_IT_OUT_BUTTON = (By.XPATH, "//*[contains(text(),'Try it out')]")


class MetamaskInstallCompletedPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_next(self):
        """
        click on next button
        """
        self.click("NEXT_BUTTON", NEXT_BUTTON)

    def is_done_button_exist(self):
        """
        check is Done button exist
        :return: true if existed, otherwise return false
        """
        return self.is_element_exist("DONE_BUTTON", DONE_BUTTON)

    def click_on_done(self):
        """
        click on done button
        """
        self.click("DONE_BUTTON", DONE_BUTTON)

    def is_try_it_out_button_exist(self):
        """
        check is Try it out
        :return: true if existed, otherwise return false
        """
        return self.is_element_exist("TRY_IT_OUT_BUTTON", TRY_IT_OUT_BUTTON)

    def click_on_try_it_out_button(self):
        """
        click on Try it out button
        """
        self.click("TRY_IT_OUT_BUTTON", TRY_IT_OUT_BUTTON)
