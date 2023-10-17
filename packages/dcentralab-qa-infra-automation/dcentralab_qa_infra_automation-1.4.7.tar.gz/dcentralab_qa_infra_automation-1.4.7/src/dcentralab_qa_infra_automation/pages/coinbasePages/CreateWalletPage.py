from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
create or import wallet page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Create new wallet')]")
ALREADY_HAVE_WALLET_LINK = (By.XPATH, "//*[contains(text(),'I already have a wallet')]")


class CreateWalletPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_already_have_a_wallet(self):
        """
        click on already have a wallet
        """
        self.click("ALREADY_HAVE_WALLET_LINK", ALREADY_HAVE_WALLET_LINK)
