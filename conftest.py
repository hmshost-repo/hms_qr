from datetime import datetime
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from src.utils.constants import (
    BROWSER_OPTIONS,
    TIMEOUTS
)
import logging


# def pytest_configure(config):
#     config.option.tb_style = "no"
#
#     logging.getLogger('root').setLevel(logging.ERROR)
#     logging.getLogger('selenium').setLevel(logging.ERROR)
#     logging.getLogger('urllib3').setLevel(logging.ERROR)
#     logging.getLogger('src.pages.base_page').setLevel(logging.CRITICAL)
#     logging.getLogger('src.pages.store.menu_page').setLevel(logging.CRITICAL)
#
#     config.option.capture = "no"
#
#     if config.getoption('numprocesses', default=None):
#         config.option.numprocesses = 3  # Limit to 3 parallel processes
#
#
# def pytest_addoption(parser):
#     parser.addoption("--id", action="store", help="store id in format XXX/XXX")
#
#
# @pytest.fixture(scope="session")
# def store_id(request):
#     return request.config.getoption("--id")
#
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#
#     if report.when == "call" and report.failed:
#         try:
#             driver = item.funcargs['driver']
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#
#             store_id = ''
#             if hasattr(item, 'callspec'):
#                 params = item.callspec.params
#                 if 'store_id' in params:
#                     store_id = f"_{str(params['store_id']).replace('/', '_')}"
#
#             filename = f"{item.name}{store_id}_{timestamp}.png"
#
#             filepath = SCREENSHOTS_DIR / filename
#
#             driver.save_screenshot(str(filepath))
#             print(f"\nScreenshot saved: {filepath}")
#         except Exception as e:
#             print(f"\nFailed to capture screenshot: {str(e)}")


@pytest.fixture
def driver(request):
    browser = 'chrome'  # default browser
    driver = None

    try:
        if browser == 'chrome':
            options = ChromeOptions()
            for option in BROWSER_OPTIONS['chrome']['default']:
                options.add_argument(option)
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        elif browser == 'firefox':
            options = FirefoxOptions()
            for pref, value in BROWSER_OPTIONS['firefox']['preferences'].items():
                options.set_preference(pref, value)
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            driver.maximize_window()

        elif browser == 'edge':
            options = EdgeOptions()
            for option in BROWSER_OPTIONS['edge']['default']:
                options.add_argument(option)
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

        if driver:
            driver.implicitly_wait(TIMEOUTS['implicit'])
            driver.set_page_load_timeout(TIMEOUTS['page_load'])
            driver.set_script_timeout(TIMEOUTS['page_load'])
            yield driver
            driver.quit()

    except Exception:
        if driver:
            driver.quit()
        raise


