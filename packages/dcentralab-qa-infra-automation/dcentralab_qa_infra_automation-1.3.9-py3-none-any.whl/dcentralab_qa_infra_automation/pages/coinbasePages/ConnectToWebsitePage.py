from dcentralab_qa_infra_automation.pages.BasePage import BasePage
from selenium.webdriver.common.by import By

"""
connect to website page

@Author: Efrat Cohen
@Date: 02.2023
"""

"""page locators"""
TITLE = (By.XPATH, "//*[contains(text(),'Connect to website')]")
CONNECT_BUTTON = (By.XPATH, "//*[contains(@class,'cds-typographyResets-t1xhpuq2 cds-headline-hb7l4gg cds-primaryForeg')]")


class ConnectToWebsitePage(BasePage):

    def __init__(self, driver):
        """ ctor - call to BasePage ctor for initialize """
        super().__init__(driver)

    def is_page_loaded(self):
        """
        check if on current page
        @return: true if on page, otherwise return false
        """
        return self.is_element_exist("TITLE", TITLE)

    def click_on_connect_button(self):
        """
        click on connect button
        """
        self.click("CONNECT_BUTTON", CONNECT_BUTTON)
