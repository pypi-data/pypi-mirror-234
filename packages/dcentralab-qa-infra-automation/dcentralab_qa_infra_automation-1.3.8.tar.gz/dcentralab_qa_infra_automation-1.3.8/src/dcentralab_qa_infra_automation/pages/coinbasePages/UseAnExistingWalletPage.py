from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
use an existing wallet page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Use an existing wallet')]")
ENTER_RECOVERY_PHRASE = (By.XPATH, "//*[contains(text(),'Enter recovery phrase')]")


class UseAnExistingWalletPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_enter_recovery_phrase(self):
        """
        click on enter recovery phrase
        """
        self.click("ENTER_RECOVERY_PHRASE", ENTER_RECOVERY_PHRASE)
