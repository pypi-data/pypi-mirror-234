from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By
import pytest

"""
import wallet page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Access your wallet')]")
SECRET_RECOVERY_PHRASE_0 = (By.ID, "import-srp__srp-word-0")
SECRET_RECOVERY_PHRASE_1 = (By.ID, "import-srp__srp-word-1")
SECRET_RECOVERY_PHRASE_2 = (By.ID, "import-srp__srp-word-2")
SECRET_RECOVERY_PHRASE_3 = (By.ID, "import-srp__srp-word-3")
SECRET_RECOVERY_PHRASE_4 = (By.ID, "import-srp__srp-word-4")
SECRET_RECOVERY_PHRASE_5 = (By.ID, "import-srp__srp-word-5")
SECRET_RECOVERY_PHRASE_6 = (By.ID, "import-srp__srp-word-6")
SECRET_RECOVERY_PHRASE_7 = (By.ID, "import-srp__srp-word-7")
SECRET_RECOVERY_PHRASE_8 = (By.ID, "import-srp__srp-word-8")
SECRET_RECOVERY_PHRASE_9 = (By.ID, "import-srp__srp-word-9")
SECRET_RECOVERY_PHRASE_10 = (By.ID, "import-srp__srp-word-10")
SECRET_RECOVERY_PHRASE_11 = (By.ID, "import-srp__srp-word-11")
CONFIRM_BUTTON = (By.XPATH, "//*[contains(text(),'Confirm Secret Recovery Phrase')]")


class ImportWalletPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def insert_secret_recovery_phrase(self):
        """
        insert secret recovery phrase
        """
        self.enter_text("SECRET_RECOVERY_PHRASE_0", SECRET_RECOVERY_PHRASE_0, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_0"))
        self.enter_text("SECRET_RECOVERY_PHRASE_1", SECRET_RECOVERY_PHRASE_1, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_1"))
        self.enter_text("SECRET_RECOVERY_PHRASE_2", SECRET_RECOVERY_PHRASE_2, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_2"))
        self.enter_text("SECRET_RECOVERY_PHRASE_3", SECRET_RECOVERY_PHRASE_3, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_3"))
        self.enter_text("SECRET_RECOVERY_PHRASE_4", SECRET_RECOVERY_PHRASE_4, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_4"))
        self.enter_text("SECRET_RECOVERY_PHRASE_5", SECRET_RECOVERY_PHRASE_5, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_5"))
        self.enter_text("SECRET_RECOVERY_PHRASE_6", SECRET_RECOVERY_PHRASE_6, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_6"))
        self.enter_text("SECRET_RECOVERY_PHRASE_7", SECRET_RECOVERY_PHRASE_7, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_7"))
        self.enter_text("SECRET_RECOVERY_PHRASE_8", SECRET_RECOVERY_PHRASE_8, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_8"))
        self.enter_text("SECRET_RECOVERY_PHRASE_9", SECRET_RECOVERY_PHRASE_9, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_9"))
        self.enter_text("SECRET_RECOVERY_PHRASE_10", SECRET_RECOVERY_PHRASE_10, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_10"))
        self.enter_text("SECRET_RECOVERY_PHRASE_11", SECRET_RECOVERY_PHRASE_11, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("secret_recovery_phrase_11"))

    def click_on_confirm(self):
        """
        click on confirm button
        """
        self.click("CONFIRM_BUTTON", CONFIRM_BUTTON)