import pytest
from dcentralab_qa_infra_automation.drivers.HelperFunctions import addExtensionToChrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

"""
init chrome driver, using ChromeDriverManager for chromeDriver installation

@Author: Efrat Cohen
@Date: 11.2022
"""


def get_chrome_service():
    print(ChromeDriverManager.get_os_type())
    print(ChromeDriverManager().driver.get_url_for_version_and_platform())
    print(ChromeDriverManager().driver.get_binary_name(os_type=ChromeDriverManager.get_os_type()))
    print(ChromeDriverManager().driver.get_browser_version_from_os())
    chrome_service = Service(
        executable_path=ChromeDriverManager().install())
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
    options = webdriver.ChromeOptions()
    options.add_extension(addExtensionToChrome())
    chrome_service = get_chrome_service()
    print(chrome_service.path)
    driver = webdriver.Chrome(options=options, service=chrome_service)
    return driver
