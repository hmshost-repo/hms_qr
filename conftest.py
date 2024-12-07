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

# Configuration
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

def pytest_addoption(parser):
    parser.addoption("--id", action="store", help="store id in format XXX/XXX")

@pytest.fixture(scope="session")
def store_id(request):
    return request.config.getoption("--id")

@pytest.fixture
def driver(request):
    browser = 'chrome'  # default browser setting
    driver = None
    
    # Only change browser if specific marker is present
    if request.node.get_closest_marker('firefox'):
        browser = 'firefox'
    elif request.node.get_closest_marker('edge'):
        browser = 'edge'
    elif request.node.get_closest_marker('all_browsers'):
        # For all_browsers, Chrome will be used by default
        pass
    
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
            driver = webdriver.Edge(service = EdgeService(EdgeChromiumDriverManager().install()), options=options)
        
        if driver:
            driver.implicitly_wait(TIMEOUTS['implicit'])
            driver.set_page_load_timeout(TIMEOUTS['page_load'])
            yield driver
            driver.quit()
            
    except Exception as e:
        if driver:
            driver.quit()
        raise


@pytest.fixture
def sim_type(store_id):
    """Determine simulation type based on store ID"""
    if store_id:
        with open('src/data/stores.csv') as f:
            if store_id in f.read():
                return 'store'
        with open('src/data/sim2_stores.csv') as f:
            if store_id in f.read():
                return 'sim2'
        raise ValueError(f"Store {store_id} not found in either simulation")