import os

import pytest
from dcentralab_qa_infra_automation.fixtures import Screenshot


def add_image_when_test_failed(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = pytest.user_dir + '/target/screenshots/' + Screenshot.get_current_datetime() + " " + report.head_line.replace(
                "::", "_") + ".png"
            img_path = os.path.join(pytest.user_dir + '/target/screenshots/', "screenshots", file_name)
            pytest.driver.save_screenshot(img_path)
            screenshot = pytest.driver.get_screenshot_as_base64()
            extra.append(pytest_html.extras.image(screenshot, ''))
        if "test_article_all_components" in item.name:
            extra.append(pytest_html.extras.html(f'<h3>Test Name: {pytest.test_name}</h3>'))
            extra.append(pytest_html.extras.html(f'<h3>Component Name: {pytest.component_name}</h3>'))
            try:
                extra.append(pytest_html.extras.html(f'<h3>Article Id: {pytest.article_id}</h3>'))
            except:
                pass
        report.extra = extra


def customize_report_environment_table(config):
    """ modifying the table pytest environment"""
    # getting python version
    from platform import python_version
    py_version = python_version()
    # Overwriting old parameters with  new parameters
    config._metadata = {
        "python_version": py_version
    }
