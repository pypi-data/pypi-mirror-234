from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
welcome to metamask page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'get started')]")
AGREE_TERMS_CHECKBOX = (By.ID, "onboarding__terms-checkbox")
IMPORT_WALLET_BUTTON = (By.XPATH, "//*[contains(text(),'Import an existing wallet')]")
CONNECT_WALLET_POPUP = (By.XPATH, "//*[contains(@class,'permissions-connect-header__title')]")


class WelcomeToMetamaskPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_agree_terms(self):
        """
        click on agree terms button
        """
        self.click("AGREE_TERMS_CHECKBOX", AGREE_TERMS_CHECKBOX)

    def is_button_exists(self):
        return self.is_element_exist("IMPORT_WALLET_BUTTON", IMPORT_WALLET_BUTTON)

    def click_on_import_wallet(self):
        """
        click on import wallet button
        """
        self.click("GET_STARTED_BUTTON", IMPORT_WALLET_BUTTON)