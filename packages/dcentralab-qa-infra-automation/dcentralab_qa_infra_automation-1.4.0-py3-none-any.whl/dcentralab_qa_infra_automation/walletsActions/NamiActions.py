import time

import pytest

from dcentralab_qa_infra_automation.pages.namiPages.CreateAccountPage import CreateAccountPage
from dcentralab_qa_infra_automation.pages.namiPages.ImportSeedPhrasePage import ImportSeedPhrasePage
from dcentralab_qa_infra_automation.pages.namiPages.NamiBasePage import NamiBasePage
from dcentralab_qa_infra_automation.pages.namiPages.WelcomePage import WelcomePage
from dcentralab_qa_infra_automation.pages.namiPages.SuccessfullyCreatedWalletPage import SuccessfullyCreatedWalletPage
from dcentralab_qa_infra_automation.pages.namiPages.ConnectWalletPage import ConnectWalletPage
from dcentralab_qa_infra_automation.pages.namiPages.SignPage import SignPage

"""
Nami wallet actions
@Author: Efrat Cohen
@Date: 06.2023
"""
from dcentralab_qa_infra_automation.utils.WalletsActionsInterface import WalletsActionsInterface


class NamiActions(WalletsActionsInterface):
    """
    coinbase actions class
    this class implements wallet actions interface.
    """

    def __init__(self, driver):
        self.driver = driver

    def import_wallet(self):
        """
        import wallet process
        """
        # Open new tab
        self.driver.execute_script("window.open('');")

        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Open chrome extension
        self.driver.get(pytest.properties.get("nami.connect.url"))

        welcomePage = WelcomePage(self.driver)

        # Check if Nami wallet welcome page loaded
        assert welcomePage.is_page_loaded(), "Nami welcome page loaded"

        # Click on import button
        welcomePage.click_on_import_wallet()

        # Check is import a wallet popup loaded
        assert welcomePage.is_import_a_wallet_popup_loaded(), "import a wallet popup loaded"

        # Click on choose seed phrase length
        welcomePage.click_on_choose_seed_phrase_length()

        # Choose word phrase (24)
        welcomePage.choose_word_seed_phrase()

        # Click on accept terms button
        welcomePage.click_on_accept_terms_button()

        # Click on continue button
        welcomePage.click_on_continue_button()

        time.sleep(3)

        # Switch to the new window
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[2])

        importSeedPhrasePage = ImportSeedPhrasePage(self.driver)

        # Check if import seed phrase page loaded
        assert importSeedPhrasePage.is_page_loaded(), "import seed phrase page loaded"

        # Insert word seed phrase
        importSeedPhrasePage.insert_word_seed_phrase()

        # Click on next button
        importSeedPhrasePage.click_on_next_button()

        createAccountPage = CreateAccountPage(self.driver)
        # Check if create account page loaded
        assert createAccountPage.is_page_loaded(), "create account page loaded"

        # Insert account name
        createAccountPage.insert_account_name()

        # Insert account password
        createAccountPage.insert_password()

        # Confirm password
        createAccountPage.insert_confirm_password()

        # Click on create account button
        createAccountPage.click_on_create_button()

        successfullyCreatedWalletPage = SuccessfullyCreatedWalletPage(self.driver)
        # Check if successfully created wallet page loaded
        assert successfullyCreatedWalletPage.is_page_loaded(), "successfully create wallet page loaded"

        # Click on close button
        successfullyCreatedWalletPage.click_on_close_button()

        # Focus on the second tab window
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Close the tad
        self.driver.close()

        # Focus on the first tab window
        self.driver.switch_to.window(self.driver.window_handles[0])

    def switch_network(self):
        """
        switch network process
        """
        # Open new tab
        self.driver.execute_script("window.open('');")

        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Open chrome extension
        self.driver.get(pytest.properties.get("nami.connect.url"))

        namiBasePage = NamiBasePage(self.driver)

        # Check if Nami wallet welcome page loaded
        assert namiBasePage.is_page_loaded(), "Nami base page loaded"

        # Click on menu button
        namiBasePage.click_on_menu()

        # Choose settings menu option
        namiBasePage.click_on_setting()
        assert namiBasePage.is_on_settings_window(), "settings window loaded"

        # Click on network
        namiBasePage.click_on_network()
        assert namiBasePage.is_on_network_window(), "network window loaded"

        # Click on network select
        namiBasePage.click_on_network_select()

        # Choose network
        namiBasePage.choose_network()

        time.sleep(1)

        # Close the tad
        self.driver.close()

        # Focus on the first tab window
        self.driver.switch_to.window(self.driver.window_handles[0])

    def connect_wallet(self):
        """
        connect wallet implementation
        """
        time.sleep(3)

        # Nami popup instance
        whandle = self.driver.window_handles[1]

        # Switch to pop up window
        self.driver.switch_to.window(whandle)

        connectWalletPage = ConnectWalletPage(self.driver)
        # Check is connect to website popup loaded
        assert connectWalletPage.is_page_loaded(), "connect wallet window loaded"

        # Click on accept button
        connectWalletPage.click_on_accept_button()

        time.sleep(2)

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])

    def confirm(self):
        """
        confirm wallet process
        """
        time.sleep(8)

        # Nami popup instance
        whandle = self.driver.window_handles[1]

        # Switch to pop up window
        self.driver.switch_to.window(whandle)

        signPage = SignPage(self.driver)
        # Check is sign popup loaded
        assert signPage.is_page_loaded(), "Sign window loaded"

        # Click on sign button
        signPage.click_on_sign_button()

        # Check is confirm with password popup loaded
        signPage.is_confirm_with_password_popup_loaded()

        # Insert password
        signPage.insert_password()

        # Click on confirm button
        signPage.click_on_confirm_button()

        time.sleep(2)

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])
