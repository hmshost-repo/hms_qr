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
from src.utils.error_handler import handle_test_errors
import logging


SCREENSHOTS_DIR = Path("test_failures/screenshots")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://qaquickpay.hmshost.com/Menu"

BROWSER_OPTIONS = {
    'chrome': {
        'default': [
            "--start-maximized",
            "--disable-notifications",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-infobars",
            "--disable-browser-side-navigation",
            "--disable-site-isolation-trials",
            "--page-load-strategy=none",
            "--disable-extensions",
            "--dns-prefetch-disable"
        ]
    },
    'firefox': {
        'preferences': {
            "browser.startup.homepage": "about:blank",
            "startup.homepage_welcome_url": "about:blank",
            "browser.download.folderList": 2,
            "browser.download.manager.showWhenStarting": False
        }
    },
    'edge': {
        'default': [
            "--start-maximized",
            "--disable-notifications",
            # "--headless=new",
            "--disable-gpu",
            "--no-sandbox"
        ]
    }
}

TIMEOUTS = {
    'implicit': 0,
    'explicit': 1,
    'page_load': 3
}


def pytest_configure(config):
    # Configure pytest to show cleaner output
    config.option.tb_style = "no"
    
    # Configure logging to suppress all logs except critical
    logging.getLogger('root').setLevel(logging.ERROR)
    logging.getLogger('selenium').setLevel(logging.ERROR)
    logging.getLogger('urllib3').setLevel(logging.ERROR)
    logging.getLogger('src.pages.base_page').setLevel(logging.CRITICAL)
    logging.getLogger('src.pages.store.menu_page').setLevel(logging.CRITICAL)
    
    # Disable pytest logging capture
    config.option.capture = "no"


def pytest_addoption(parser):
    parser.addoption("--id", action="store", help="store id in format XXX/XXX")


@pytest.fixture(scope="session")
def store_id(request):
    return request.config.getoption("--id")


# @pytest.fixture
# def driver(request):
#     browser = 'chrome'  # default browser setting
#     driver = None
#
#     # Only change browser if specific marker is present
#     if request.node.get_closest_marker('firefox'):
#         browser = 'firefox'
#     elif request.node.get_closest_marker('edge'):
#         browser = 'edge'
#     elif request.node.get_closest_marker('all_browsers'):
#         # For all_browsers, Chrome will be used by default
#         pass
#
#     try:
#         if browser == 'chrome':
#             options = ChromeOptions()
#             for option in BROWSER_OPTIONS['chrome']['default']:
#                 options.add_argument(option)
#             driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
#
#         elif browser == 'firefox':
#             options = FirefoxOptions()
#             for pref, value in BROWSER_OPTIONS['firefox']['preferences'].items():
#                 options.set_preference(pref, value)
#             driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
#             driver.maximize_window()
#
#         elif browser == 'edge':
#             options = EdgeOptions()
#             for option in BROWSER_OPTIONS['edge']['default']:
#                 options.add_argument(option)
#             driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
#
#         if driver:
#             driver.implicitly_wait(TIMEOUTS['implicit'])
#             driver.set_page_load_timeout(TIMEOUTS['page_load'])
#             yield driver
#             driver.quit()
#
#     except Exception as e:
#         if driver:
#             driver.quit()
#         raise


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            driver = item.funcargs['driver']
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Get store_id if available
            store_id = ''
            if hasattr(item, 'callspec'):
                params = item.callspec.params
                if 'store_id' in params:
                    store_id = f"_{str(params['store_id']).replace('/', '_')}"

            # Create filename with test name, store ID, and timestamp
            filename = f"{item.name}{store_id}_{timestamp}.png"
            filepath = SCREENSHOTS_DIR / filename

            driver.save_screenshot(str(filepath))
            print(f"\nScreenshot saved: {filepath}")
        except Exception as e:
            print(f"\nFailed to capture screenshot: {str(e)}")


@pytest.fixture
def driver(request):
    browser = 'chrome'  # default browser
    driver = None

    # Set browser based on markers
    if request.node.get_closest_marker('firefox'):
        browser = 'firefox'
    elif request.node.get_closest_marker('edge'):
        browser = 'edge'

    try:
        if browser == 'chrome':
            options = ChromeOptions()
            for option in BROWSER_OPTIONS['chrome']['default']:
                options.add_argument(option)
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
            yield driver
            driver.quit()

    except Exception as e:
        if driver:
            driver.quit()
        raise


def pytest_collection_modifyitems(items):
    for item in items:
        item.obj = handle_test_errors(item.obj)