import pytest
from dcentralab_qa_infra_automation.utils.HTTPMethods import get

"""
helper functions to add options to driver

@Author: Efrat Cohen
@Date: 04.2023
"""


def addExtensionToChrome():
    """
    add CRX extension to chrome
    :return: add_extension - current extension crx file
    """
    add_extension = None
    # In metamask wallet type
    if pytest.data_driven.get("wallet_type") == 'MetaMask':
        add_extension = pytest.user_dir + pytest.properties.get("metamask.extension.crx")
    elif pytest.data_driven.get("wallet_type") == 'Coinbase':
        add_extension = pytest.user_dir + pytest.properties.get("coinbase.extension.crx")
    elif pytest.data_driven.get("wallet_type") == 'Nami':
        add_extension = pytest.user_dir + pytest.properties.get("nami.extension.crx")

    return add_extension


def inject_rpc():
    """
    add CRX extension to chrome
    :return: add_extension - current extension crx file
    """
    add_extension = None
    # In metamask wallet type
    if pytest.data_driven.get("wallet_type") == 'MetaMask':
        add_extension = pytest.user_dir + pytest.properties.get("metamask.extension.crx")
    elif pytest.data_driven.get("wallet_type") == 'Coinbase':
        add_extension = pytest.user_dir + pytest.properties.get("coinbase.extension.crx")
    elif pytest.data_driven.get("wallet_type") == 'Nami':
        add_extension = pytest.user_dir + pytest.properties.get("nami.extension.crx")

    return add_extension


def get_chrome_driver_version():
    # Perform rest get method to get the chrome driver version
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = get(url)

    # Check response status
    if response.status_code == 200:
        # Get chromedriver version
        version = response.text.strip()
        return version
    else:
        # Handle the case when the request fails
        raise ValueError(f"Failed to fetch the Chrome driver version. Status code: {response.status_code}")