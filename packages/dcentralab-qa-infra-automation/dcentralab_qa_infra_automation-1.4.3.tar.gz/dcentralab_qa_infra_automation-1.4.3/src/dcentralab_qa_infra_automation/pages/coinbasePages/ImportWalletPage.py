from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By
import pytest

"""
import wallet page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//h3[contains(text(),'Import wallet')]")
ENTER_WORD_SEED_PHRASE = (By.XPATH, "//input[contains(@class,'cds-nativeInputBaseStyle-n1l8ztqg')]")
IMPORT_WALLET_BUTTON = (By.XPATH, "//span[contains(text(),'Import wallet')]")


class ImportWalletPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def insert_recovery_phrase(self):
        """
        enter recovery phrase
        """
        self.enter_text("ENTER_WORD_SEED_PHRASE", ENTER_WORD_SEED_PHRASE, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase"))


    def click_on_import_wallet(self):
        """
        click on import wallet
        """
        self.click("IMPORT_WALLET_BUTTON", IMPORT_WALLET_BUTTON)

