import datetime

import pytest

"""
screenshots fixture function for screenshot of the test falling
after each test, if the test failed - take screenshot and store him with datetime

@Author: Efrat Cohen
@Date: 09.2022
"""


def get_current_datetime():
    """
    init current datetime
    @return date_time - current time
    """
    # Current date and time
    current_time = datetime.datetime.now()
    date_time = current_time.strftime("%d-%m-%Y %H-%M-%S")
    return date_time


def after_test(request):
    """
    Take screenshot when test fail, save it in screenshot folder with current datetime in file name
    :param request: the requesting test context
    """
    if request.session.testsfailed:
        pytest.logger.info("test " + request.node.nodeid + " failed, take screenshot")
        # Get driver name
        driver_type = request.cls.driver.name
        # Save screenshot in target directory
        request.cls.driver.save_screenshot(
            pytest.user_dir + '/target/screenshots/' + "SC " + get_current_datetime() + " " + driver_type + ".png")
        pytest.logger.info("screenshot successfully taken")
