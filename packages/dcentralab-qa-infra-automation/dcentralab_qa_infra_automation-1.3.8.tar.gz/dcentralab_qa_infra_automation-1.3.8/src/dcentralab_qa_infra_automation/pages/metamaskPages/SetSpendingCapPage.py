from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
Set a spending cap for your page

@Author: Efrat Cohen
@Date: 09.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Verify third-party details')]")
MAX_BTN = (By.XPATH, "//*[contains(text(),'Max')]")
NEXT_BTN = (By.XPATH, "//*[contains(text(),'Next')]")
APPROVE_BTN = (By.XPATH, "//*[contains(text(),'Approve')]")


class SetSpendingCapPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_max_button(self):
        """
        choose max custom spending cap
        """
        self.click("MAX_BTN", MAX_BTN)

    def click_next_button(self):
        """
        click on next button
        """
        self.click("NEXT_BTN", NEXT_BTN)

    def click_approve_button(self):
        """
        click on approve button
        """
        self.click("APPROVE_BTN", APPROVE_BTN)
