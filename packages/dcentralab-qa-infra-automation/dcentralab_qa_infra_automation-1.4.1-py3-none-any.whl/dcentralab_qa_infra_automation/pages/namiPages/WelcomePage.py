from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
welcome page

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(@class, 'chakra-text css-1mmhjtn')]")
IMPORT_WALLET_BTM = (By.XPATH, "//button[contains(text(),'Import')]")
IMPORT_A_WALLET_POPUP_TITLE = (By.XPATH, "//*[contains(@class, 'chakra-modal__header css-ykovoq')]")
CHOOSE_SEED_PHRASE_SELECT = (By.CSS_SELECTOR, "select.chakra-select")
WORD_SEED_PHRASE_OPTION = (By.XPATH, "//*[contains(text(), '24-word seed phrase')]")
ACCEPT_TERMS_BTN = (By.XPATH, "//*[contains(@class, 'chakra-checkbox__control')]")
CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue')]")


class WelcomePage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_import_wallet(self):
        """
        click on import wallet button
        """
        self.click("IMPORT_WALLET_BTM", IMPORT_WALLET_BTM)

    def is_import_a_wallet_popup_loaded(self):
        """
        check is import a wallet popup loaded
        """
        return self.is_element_exist("IMPORT_A_WALLET_POPUP_TITLE", IMPORT_A_WALLET_POPUP_TITLE)

    def click_on_choose_seed_phrase_length(self):
        """
        click on choose seed phrase length
        """
        self.click("CHOOSE_SEED_PHRASE_SELECT", CHOOSE_SEED_PHRASE_SELECT)

    def choose_word_seed_phrase(self):
        """
        choose word seed phrase
        """
        self.click("WORD_SEED_PHRASE_OPTION", WORD_SEED_PHRASE_OPTION)

    def click_on_accept_terms_button(self):
        """
        click on accept terms button
        """
        self.click("ACCEPT_TERMS_BTN", ACCEPT_TERMS_BTN)

    def click_on_continue_button(self):
        """
        click on continue button
        """
        self.click("CONTINUE_BUTTON", CONTINUE_BUTTON)


