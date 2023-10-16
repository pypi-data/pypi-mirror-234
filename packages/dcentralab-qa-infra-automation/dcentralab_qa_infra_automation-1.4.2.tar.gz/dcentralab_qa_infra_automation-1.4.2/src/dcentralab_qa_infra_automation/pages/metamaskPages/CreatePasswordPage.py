from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By
import pytest

"""
create password page

@Author: Efrat Cohen
@Date: 07.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Create password')]")
PASSWORD_INPUT = (By.XPATH, "//*[contains(@class,'form-field__input')]")
UNDERSTAND_METAMASK_CHECKBOX = (By.XPATH, "//*[contains(@class,'check-box far fa-square')]")
IMPORT_WALLET_BTN = (By.XPATH, "//*[contains(text(),'Import my wallet')]")


class CreatePasswordPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def insert_password(self):
        """
        insert password
        """
        self.enter_text_on_specific_list_item("PASSWORD_INPUT", PASSWORD_INPUT, 0, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("password"))

    def insert_confirm_password(self):
        """
        insert confirm password
        """
        self.enter_text_on_specific_list_item("CONFIRM_PASSWORD_INPUT", PASSWORD_INPUT, 1, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("password"))

    def click_on_understand_metamask_checkbox(self):
        """
        click on understand metamask checkbox
        """
        self.click("UNDERSTAND_METAMASK_CHECKBOX", UNDERSTAND_METAMASK_CHECKBOX)

    def click_on_import_wallet(self):
        """
        click on import wallet
        """
        self.click("IMPORT_WALLET_BTN", IMPORT_WALLET_BTN)
