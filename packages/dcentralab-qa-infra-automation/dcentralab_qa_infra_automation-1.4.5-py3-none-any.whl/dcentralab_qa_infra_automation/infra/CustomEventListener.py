from selenium.webdriver.support.events import (AbstractEventListener)
import logging.config


class CustomEventListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        logging.info(f"Before navigating from '{driver.current_url}' to '{url}'. Driver session: '{driver.session_id}'")

    def after_navigate_to(self, url, driver):
        logging.info(f"After navigating to '{url}'. Current URL is '{driver.current_url}'. "
                     f"Driver session: '{driver.session_id}' ")

    def before_navigate_back(self, driver):
        logging.info(f"Before navigating back from '{driver.current_url}'. Driver session: '{driver.session_id}' ")

    def after_navigate_back(self, driver):
        logging.info(f"After navigating back to '{driver.current_url}'. Driver session: '{driver.session_id}' ")

    def before_navigate_forward(self, driver):
        logging.info(f"Before navigating forward from '{driver.current_url}'. Driver session: '{driver.session_id}' ")

    def after_navigate_forward(self, driver):
        logging.info(f"After navigating forward to '{driver.current_url}'. Driver session: '{driver.session_id}' ")

    def before_find(self, by, value, driver):
        logging.info(f"Before find element using '{by}' and value '{value}'. Driver session: '{driver.session_id}' ")

    def after_find(self, by, value, driver):
        logging.info(f"After find element using '{by}' and value '{value}'. Driver session: '{driver.session_id}' ")

    def before_click(self, element, driver):
        logging.info(f"Before clicking element '{element}'. Driver session: '{driver.session_id}' ")

    def after_click(self, element, driver):
        logging.info(f"After clicking element '{element}'. Driver session: '{driver.session_id}' ")

    def before_change_value_of(self, element, driver):
        logging.info(f"Before changing value of element '{element}'. Driver session: '{driver.session_id}' ")

    def after_change_value_of(self, element, driver):
        logging.info(f"After changing value of element '{element}'. Driver session: '{driver.session_id}' ")

    def before_execute_script(self, script, driver):
        logging.info(f"Before executing script '{script}'. Driver session: '{driver.session_id}' ")

    def after_execute_script(self, script, driver):
        logging.info(f"After executing script '{script}'. Driver session: '{driver.session_id}' ")

    def before_close(self, driver):
        logging.info(f"Before driver close. Driver session: '{driver.session_id}'")

    def after_close(self, driver):
        logging.info(f"After driver close. Driver session: '{driver.session_id}'")

    def before_quit(self, driver):
        logging.info(f"Before driver quit. Driver session: '{driver.session_id}'")

    def after_quit(self, driver):
        logging.info(f"After driver quit. Driver session: '{driver.session_id}'")

    def on_exception(self, exception, driver):
        logging.error(f"Exception occured. Exception is '{exception}'. Driver session: '{driver.session_id}' ")
