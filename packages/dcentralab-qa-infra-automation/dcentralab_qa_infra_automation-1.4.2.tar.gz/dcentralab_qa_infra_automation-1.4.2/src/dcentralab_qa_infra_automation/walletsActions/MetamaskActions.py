import time

import pytest
from dcentralab_qa_infra_automation.utils.WalletsActionsInterface import WalletsActionsInterface
from dcentralab_qa_infra_automation.pages.metamaskPages.ConfirmPage import ConfirmPage
from dcentralab_qa_infra_automation.pages.metamaskPages.ImportWalletPage import ImportWalletPage
from dcentralab_qa_infra_automation.pages.metamaskPages.CongratulationsPage import CongratulationsPage
from dcentralab_qa_infra_automation.pages.metamaskPages.ConnectWithWalletPage import ConnectWithMetamaskPage
from dcentralab_qa_infra_automation.pages.metamaskPages.ImproveMetamaskPage import ImproveMetamaskPage
from dcentralab_qa_infra_automation.pages.metamaskPages.SwitchNetworkPage import SwitchNetworkPage
from dcentralab_qa_infra_automation.pages.metamaskPages.WelcomeToMetamaskPage import WelcomeToMetamaskPage
from dcentralab_qa_infra_automation.pages.metamaskPages.CreatePasswordPage import CreatePasswordPage
from dcentralab_qa_infra_automation.pages.metamaskPages.MetamaskInstallCompletedPage import MetamaskInstallCompletedPage
from dcentralab_qa_infra_automation.pages.metamaskPages.SetSpendingCapPage import SetSpendingCapPage

"""
MetaMask wallet actions
@Author: Efrat Cohen
@Date: 12.2022
"""


class MetamaskActions(WalletsActionsInterface):

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
        self.driver.get(pytest.properties.get("metamask.connect.url"))

        # Focus on the first tab window
        self.driver.switch_to.window(self.driver.window_handles[1])

        welcomeToMetamaskPage = WelcomeToMetamaskPage(self.driver)

        # Check if metamask wallet page loaded
        assert welcomeToMetamaskPage.is_page_loaded(), "Let's get started page loaded"

        # Click on agree terms
        welcomeToMetamaskPage.click_on_agree_terms()

        assert welcomeToMetamaskPage.is_button_exists()

        # Click on import wallet button
        welcomeToMetamaskPage.click_on_import_wallet()

        improveMetamaskPage = ImproveMetamaskPage(self.driver)

        # Check if improve to metamask page loaded
        assert improveMetamaskPage.is_page_loaded(), "Help us improve MetaMask page loaded"

        # Click on I agree button
        improveMetamaskPage.click_on_i_agree_button()

        importWalletPage = ImportWalletPage(self.driver)

        # Check if import wallet page loaded
        assert importWalletPage.is_page_loaded(), "Access your wallet with your Secret Recovery Phrase"

        # Insert secret recovery phrase
        importWalletPage.insert_secret_recovery_phrase()

        # Click on confirm button
        importWalletPage.click_on_confirm()

        createPasswordPage = CreatePasswordPage(self.driver)

        assert createPasswordPage.is_page_loaded(), "Create password page loaded"

        # Insert password
        createPasswordPage.insert_password()

        # Insert confirm password
        createPasswordPage.insert_confirm_password()

        # Click on understand MetaMask checkbox
        createPasswordPage.click_on_understand_metamask_checkbox()

        # Click on import wallet
        createPasswordPage.click_on_import_wallet()

        congratulationsPage = CongratulationsPage(self.driver)

        # Check if congratulations page loaded
        assert congratulationsPage.is_page_loaded(), "congratulations page loaded"

        # Click on got it button
        congratulationsPage.click_on_got_it_button()

        metamaskInstallCompletedPage = MetamaskInstallCompletedPage(self.driver)

        # Check if metamask install completed page loaded
        assert metamaskInstallCompletedPage.is_page_loaded(), "metamask install completed page loaded"

        # Click on next button
        metamaskInstallCompletedPage.click_on_next()

        # Check is Done button exist
        assert metamaskInstallCompletedPage.is_done_button_exist(), "Done button loaded"

        # Click on Done button
        metamaskInstallCompletedPage.click_on_done()

        # Check is Try it out button exist
        assert metamaskInstallCompletedPage.is_try_it_out_button_exist(), "Try it out button loaded"

        # Click on Try it out button
        metamaskInstallCompletedPage.click_on_try_it_out_button()

        # Close Metamask tab
        self.driver.close()

        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[0])

        time.sleep(2)

    def connect_wallet(self):
        """
        connect wallet implementation
        """
        connectWithMetamaskPage = ConnectWithMetamaskPage(self.driver)

        time.sleep(4)
        # Close connect with metamask extension popup
        connectWithMetamaskPage.click_on_connect_with_metamask_extension_button()

        time.sleep(3)

        # Open new tab
        self.driver.execute_script("window.open('');")

        # Switch focus to metamask tab
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Open chrome extension
        self.driver.get(pytest.properties.get("metamask.connect.url"))

        # Check if on connect with metamask page
        assert connectWithMetamaskPage.is_page_loaded(), "connect with metamask page loaded"

        # Click on next button
        connectWithMetamaskPage.click_on_next_button()

        # Click on connect button
        connectWithMetamaskPage.click_on_connect_button()

        switchNetworkPage = SwitchNetworkPage(self.driver)

        # Check if switch network page loaded
        assert switchNetworkPage.is_page_loaded(), "allow site to switch the network page loaded"

        # Click on switch network button
        switchNetworkPage.click_on_switch_network()

        # Close MetaMask tab
        self.driver.close()

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])

    def approve_token(self):
        """
        approve token in 1st ti,e porting process
        """
        # Open new tab
        self.driver.execute_script("window.open('');")

        # Focus on the new tab window
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Open chrome extension
        self.driver.get(pytest.properties.get("metamask.connect.url"))

        # Focus on the first tab window
        self.driver.switch_to.window(self.driver.window_handles[1])

        setSpendingCapPage = SetSpendingCapPage(self.driver)

        # Check if on connect with metamask page
        assert setSpendingCapPage.is_page_loaded(), "set spending cap page loaded"

        # Click on max button
        setSpendingCapPage.click_max_button()

        # Click on next button
        setSpendingCapPage.click_next_button()

        # Click on approve button
        setSpendingCapPage.click_approve_button()

        # Close MetaMask tab
        self.driver.close()

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])

    def confirm(self):
        """
        confirm wallet process
        """
        time.sleep(5)

        # Open new tab
        self.driver.execute_script("window.open('');")

        # Switch focus to metamask tab
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Open chrome extension
        self.driver.get(pytest.properties.get("metamask.connect.url"))

        confirmPage = ConfirmPage(self.driver)

        # Check is confirm page loaded
        assert confirmPage.is_page_loaded(), "confirm page loaded"

        # Check is confirm button exist.
        assert confirmPage.is_confirm_button_exist()

        # Click on confirm button
        confirmPage.click_on_confirm_button()

        # Close MetaMask tab
        self.driver.close()

        # Switch focus to site tab
        self.driver.switch_to.window(self.driver.window_handles[0])
