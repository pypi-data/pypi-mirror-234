import pytest
from dcentralab_qa_infra_automation.drivers.HelperFunctions import addExtensionToChrome
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

"""
init chrome driver, using ChromeDriverManager for chromeDriver installation

@Author: Efrat Cohen
@Date: 11.2022
"""


def get_chrome_service():
    chrome_service = Service(executable_path=ChromeDriverManager().install())
    return chrome_service


def initChromeDriver():
    """
    init chrome driver, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    driver = webdriver.Chrome(service=get_chrome_service())
    pytest.logger.info("start the chrome driver with options")
    return driver


def initChromeDriverWithExtension():
    """
    init chrome driver with CRX extension, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """

    chrome_service = get_chrome_service()
    options = ChromeOptions()
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    pytest.logger.info("add extension to chrome")
    options.add_extension(addExtensionToChrome())
    pytest.logger.info("start the chrome driver with options")
    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver
