import pytest

"""
parameters injection fixture functions - the ability to inject external param to tests via CLI

@Author: Efrat Cohen
@Date: 11.2022
"""


def pytest_addoption(parser):
    parser.addoption("--browser_type", action="store", default="chrome")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    option_value = metafunc.config.option.browser_type
    if 'browser_type' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("browser_type", [option_value])
        pytest.browser_type = option_value
