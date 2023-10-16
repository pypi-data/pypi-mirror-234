from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By
import pytest

"""
create password page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Create password')]")
PASSWORD_INPUT = (By.ID, "Password")
VERIFY_PASSWORD_INPUT = (By.ID, "Verify password")
AGREE_TERMS_CHECKBOX = (By.XPATH, "//*[contains(@class,'cds-interactableContainer')]")
SUBMIT_BUTTON = (By.XPATH, "//*[contains(text(),'Submit')]")


class CreatePasswordPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def insert_password(self):
        """
        insert password
        """
        self.enter_text("PASSWORD_INPUT", PASSWORD_INPUT, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("coinbase_password"))

    def verify_password(self):
        """
        verify password
        """
        self.enter_text("VERIFY_PASSWORD_INPUT", VERIFY_PASSWORD_INPUT, pytest.wallets_data.get(pytest.data_driven.get("wallet")).get("coinbase_password"))

    def click_on_agree_terms_checkbox(self):
        """
        click on agree terms checkbox
        """
        self.click("AGREE_TERMS_CHECKBOX", AGREE_TERMS_CHECKBOX)

    def click_on_submit(self):
        """
        click on submit
        """
        self.click("SUBMIT_BUTTON", SUBMIT_BUTTON)

