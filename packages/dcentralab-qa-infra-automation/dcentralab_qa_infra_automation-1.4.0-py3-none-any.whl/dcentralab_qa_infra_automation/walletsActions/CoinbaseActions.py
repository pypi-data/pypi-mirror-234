import time

import pytest
from dcentralab_qa_infra_automation.utils.WalletsActionsInterface import WalletsActionsInterface

from dcentralab_qa_infra_automation.pages.coinbasePages.ConnectToWebsitePage import ConnectToWebsitePage
from dcentralab_qa_infra_automation.pages.coinbasePages.CreatePasswordPage import CreatePasswordPage
from dcentralab_qa_infra_automation.pages.coinbasePages.CreateWalletPage import CreateWalletPage
from dcentralab_qa_infra_automation.pages.coinbasePages.ImportWalletPage import ImportWalletPage
from dcentralab_qa_infra_automation.pages.coinbasePages.ReceiveCryptoToUsername import ReceiveCryptoToUsernamePage
from dcentralab_qa_infra_automation.pages.coinbasePages.UseAnExistingWalletPage import UseAnExistingWalletPage
from dcentralab_qa_infra_automation.pages.coinbasePages.ConfirmPage import ConfirmPage

"""
Coinbase wallet actions
@Author: Efrat Cohen
@Date: 03.2023
"""


class CoinbaseActions(WalletsActionsInterface):
    """
    coinbase actions class
    this class implements wallet actions interface.
    """

    def __init__(self, driver):
        self.driver = driver

    def import_wallet(self):
        """
        import coinbase wallet process implementation
        """
        # Open new tab
        self.driver.execute_script("window.open('');")

        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get(pytest.properties.get("coinbase.connect.url"))

        createWalletPage = CreateWalletPage(self.driver)

        # Check if create or import wallet page loaded
        assert createWalletPage.is_page_loaded()

        # Click on already have a wallet
        createWalletPage.click_on_already_have_a_wallet()

        useAnExistingWalletPage = UseAnExistingWalletPage(self.driver)

        # Check is use an existing wallet page loaded
        assert useAnExistingWalletPage.is_page_loaded()

        # Click on enter recovery phrase
        useAnExistingWalletPage.click_on_enter_recovery_phrase()

        importWalletPage = ImportWalletPage(self.driver)

        # Check if import wallet page loaded
        assert importWalletPage.is_page_loaded()

        # Insert recovery phrase
        importWalletPage.insert_recovery_phrase()

        # Click on import wallet button
        importWalletPage.click_on_import_wallet()

        createPasswordPage = CreatePasswordPage(self.driver)

        # Check is create password page loaded
        assert createPasswordPage.is_page_loaded()

        # Insert password
        createPasswordPage.insert_password()

        # Verify password
        createPasswordPage.verify_password()

        # Click on agree terms checkbox
        createPasswordPage.click_on_agree_terms_checkbox()

        # Click on submit
        createPasswordPage.click_on_submit()

        receiveCryptoToUsernamePage = ReceiveCryptoToUsernamePage(self.driver)

        # Check if page after wallet connection loaded
        assert receiveCryptoToUsernamePage.is_page_loaded()

        time.sleep(3)

        # Close coinbase current active tab
        self.driver.close()

        # Switch focus to first tab
        self.driver.switch_to.window(self.driver.window_handles[0])

    def connect_wallet(self):
        """
            connect to wallet implementation
        """
        time.sleep(8)

        # Coinbase popup instance
        whandle = self.driver.window_handles[1]

        # Switch to pop up window
        self.driver.switch_to.window(whandle)

        connectToWebsitePage = ConnectToWebsitePage(self.driver)

        # Check is connect to website popup loaded
        assert connectToWebsitePage.is_page_loaded()

        # Click on connect button
        connectToWebsitePage.click_on_connect_button()

        time.sleep(2)

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])

    def confirm(self):
        time.sleep(5)

        # Coinbase popup instance
        whandle = self.driver.window_handles[1]

        # Switch to pop up window
        self.driver.switch_to.window(whandle)

        confirmPage = ConfirmPage(self.driver)

        # Check is got it button exist - if exists
        if confirmPage.is_got_it_button_exist():
            # Click on got_it button
            confirmPage.click_on_got_it_button()

        time.sleep(1)

        # Check is confirm button exist.
        assert confirmPage.is_confirm_button_exist()

        # Click on confirm button
        confirmPage.click_on_confirm_button()

        time.sleep(5)

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])