import pytest
from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
import seed phrase page

@Author: Efrat Cohen
@Date: 06.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(), 'Import Seed Phrase')]")
SEED_PHRASE_WORDS = (By.XPATH, "//*[contains(@class, 'chakra-input')]")
NEXT_BTN = (By.XPATH, "//*[contains(text(), 'Next')]")


class ImportSeedPhrasePage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def insert_word_seed_phrase(self):
        """
        insert 24 word seed phrase
        """
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_1", SEED_PHRASE_WORDS, 0, pytest.wallets_data.get("cardano").get("Seed_Phrase_1"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_2", SEED_PHRASE_WORDS, 1, pytest.wallets_data.get("cardano").get("Seed_Phrase_2"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_3", SEED_PHRASE_WORDS, 2, pytest.wallets_data.get("cardano").get("Seed_Phrase_3"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_4", SEED_PHRASE_WORDS, 3, pytest.wallets_data.get("cardano").get("Seed_Phrase_4"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_5", SEED_PHRASE_WORDS, 4, pytest.wallets_data.get("cardano").get("Seed_Phrase_5"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_6", SEED_PHRASE_WORDS, 5, pytest.wallets_data.get("cardano").get("Seed_Phrase_6"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_7", SEED_PHRASE_WORDS, 6, pytest.wallets_data.get("cardano").get("Seed_Phrase_7"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_8", SEED_PHRASE_WORDS, 7, pytest.wallets_data.get("cardano").get("Seed_Phrase_8"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_9", SEED_PHRASE_WORDS, 8, pytest.wallets_data.get("cardano").get("Seed_Phrase_9"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_10", SEED_PHRASE_WORDS, 9, pytest.wallets_data.get("cardano").get("Seed_Phrase_10"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_11", SEED_PHRASE_WORDS, 10, pytest.wallets_data.get("cardano").get("Seed_Phrase_11"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_12", SEED_PHRASE_WORDS, 11, pytest.wallets_data.get("cardano").get("Seed_Phrase_12"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_13", SEED_PHRASE_WORDS, 12, pytest.wallets_data.get("cardano").get("Seed_Phrase_13"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_14", SEED_PHRASE_WORDS, 13, pytest.wallets_data.get("cardano").get("Seed_Phrase_14"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_15", SEED_PHRASE_WORDS, 14, pytest.wallets_data.get("cardano").get("Seed_Phrase_15"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_16", SEED_PHRASE_WORDS, 15, pytest.wallets_data.get("cardano").get("Seed_Phrase_16"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_17", SEED_PHRASE_WORDS, 16, pytest.wallets_data.get("cardano").get("Seed_Phrase_17"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_18", SEED_PHRASE_WORDS, 17, pytest.wallets_data.get("cardano").get("Seed_Phrase_18"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_19", SEED_PHRASE_WORDS, 18, pytest.wallets_data.get("cardano").get("Seed_Phrase_19"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_20", SEED_PHRASE_WORDS, 19, pytest.wallets_data.get("cardano").get("Seed_Phrase_20"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_21", SEED_PHRASE_WORDS, 20, pytest.wallets_data.get("cardano").get("Seed_Phrase_21"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_22", SEED_PHRASE_WORDS, 21, pytest.wallets_data.get("cardano").get("Seed_Phrase_22"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_23", SEED_PHRASE_WORDS, 22, pytest.wallets_data.get("cardano").get("Seed_Phrase_23"))
        self.enter_text_on_specific_list_item("SEED_PHRASE_WORDS_24", SEED_PHRASE_WORDS, 23, pytest.wallets_data.get("cardano").get("Seed_Phrase_24"))

    def click_on_next_button(self):
        """
        click on next button
        """
        self.click("NEXT_BTN", NEXT_BTN)
