from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
congratulations page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Wallet creation successful')]")
GOT_IT_BUTTON = (By.XPATH, "//*[contains(text(),'Got it')]")


class CongratulationsPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_got_it_button(self):
        """
        click on got it button
        """
        self.click("GOT_IT_BUTTON", GOT_IT_BUTTON)
