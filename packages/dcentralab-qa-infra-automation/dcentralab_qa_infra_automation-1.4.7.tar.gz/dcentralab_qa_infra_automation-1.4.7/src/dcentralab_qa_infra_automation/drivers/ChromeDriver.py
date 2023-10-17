from dcentralab_qa_infra_automation.drivers.HelperFunctions import addExtensionToChrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

"""
init chrome driver, using ChromeDriverManager for chromeDriver installation

@Author: Efrat Cohen
@Date: 11.2022
"""


def get_chrome_service():
    print(webdriver.Chrome().service.path)
    chrome_service = Service(
        executable_path=webdriver.Chrome().service.path)
    return chrome_service


def initChromeDriver():
    """
    init chrome driver, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """

    driver = webdriver.Chrome(service=get_chrome_service())
    # pytest.logger.info("start the chrome driver with options")
    return driver


def initChromeDriverWithExtension():
    """
    init chrome driver with CRX extension, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    options = webdriver.ChromeOptions()
    options.add_extension(addExtensionToChrome())
    driver = webdriver.Chrome(options=options, service=get_chrome_service())
    return driver
