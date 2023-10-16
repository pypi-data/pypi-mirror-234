from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By
import pytest

"""
Sign page

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(), 'Details')]")
SIGN_BTN = (By.XPATH, "//button[contains(text(), 'Sign')]")
CONFIRM_WITH_PASSWORD_POPUP = (By.ID, 'chakra-modal--header-16')
ENTER_PASSWORD_INPUT = (By.XPATH, "//input[contains(@class, 'chakra-input')]")
CONFIRM_BTN = (By.XPATH, "//button[contains(text(), 'Confirm')]")


class SignPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_sign_button(self):
        """
        click on sign button
        """
        self.click("SIGN_BTN", SIGN_BTN)

    def is_confirm_with_password_popup_loaded(self):
        """
        check is confirm with password popup loaded
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("CONFIRM_WITH_PASSWORD_POPUP", CONFIRM_WITH_PASSWORD_POPUP)

    def insert_password(self):
        """
        insert password
        """
        self.enter_text("ENTER_PASSWORD_INPUT", ENTER_PASSWORD_INPUT, pytest.wallets_data.get("cardano").get("account_password"))

    def click_on_confirm_button(self):
        """
        click on confirm button
        """
        self.click("CONFIRM_BTN", CONFIRM_BTN)

