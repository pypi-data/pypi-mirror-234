from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
improve metamask page

@Author: Efrat Cohen
@Date: 12.2022
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Help us improve MetaMask')]")
I_AGREE_BUTTON = (By.XPATH, "//*[contains(text(),'I agree')]")


class ImproveMetamaskPage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        :return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_i_agree_button(self):
        """
        click on i agree button
        """
        self.click("I_AGREE_BUTTON", I_AGREE_BUTTON)
