import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from dcentralab_qa_infra_automation.drivers.HelperFunctions import addExtensionToChrome

from dcentralab_qa_infra_automation.drivers.HelperFunctions import get_chrome_driver_version

"""
init brave browser driver

@Author: Efrat Cohen
@Date: 12.2022
"""


def addBraveToChrome():
    """
    add brave to chrome based on OS type
    :return: binary_location
    """
    binary_location = None
    # On windowsOS - use windows brave path
    if pytest.data_driven.get("OS") == "windows":
        binary_location = pytest.properties.get("brave.windows.path")
    # use mac brave path
    else:
        binary_location = pytest.properties.get("brave.mac.path")
    return binary_location


def initBraveDriver():
    """
    init brave driver, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    options = webdriver.ChromeOptions()
    options.binary_location = addBraveToChrome()
    if pytest.data_driven.get("OS") == "windows":
        chrome_service = Service(executable_path=ChromeDriverManager(get_chrome_driver_version()).install())
    else:
        chrome_service = Service(executable_path=ChromeDriverManager(get_chrome_driver_version()).install())
    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver


def initBraveDriverWithExtension():
    """
    init brave driver with CRX extension, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    options = webdriver.ChromeOptions()
    options.binary_location = addBraveToChrome()
    options.add_extension(addExtensionToChrome())
    if pytest.data_driven.get("OS") == "windows":
        chrome_service = Service(executable_path=ChromeDriverManager(get_chrome_driver_version()).install())
    else:
        chrome_service = Service(executable_path=ChromeDriverManager(get_chrome_driver_version()).install())
    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver
