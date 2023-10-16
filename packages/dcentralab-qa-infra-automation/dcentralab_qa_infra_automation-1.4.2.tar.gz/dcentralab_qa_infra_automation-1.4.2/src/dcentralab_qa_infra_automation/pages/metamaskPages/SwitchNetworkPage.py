from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
allow the site to switch the network page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Allow this site to switch the network?')]")
SWITCH_NETWORK_BUTTON = (By.XPATH, "//*[contains(text(),'Switch network')]")


class SwitchNetworkPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_switch_network(self):
        """
        click on switch network button
        """
        self.click("SWITCH_NETWORK_BUTTON", SWITCH_NETWORK_BUTTON)
