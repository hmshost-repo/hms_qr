import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging
from datetime import datetime

# Configuration
BASE_URL = "https://qaquickpay.hmshost.com/Menu"

BROWSER_OPTIONS = {
    'chrome': {
        'default': [
            "--start-maximized",
            "--disable-notifications",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            # "--headless",
            "--disable-gpu",
        ]
    },
    'firefox': {
        'default': [
            "--start-maximized",
            "--disable-notifications",
            "--headless",
            "--disable-gpu",
            "-no-remote"
        ]
    },
    'edge': {
        'default': [
            "--start-maximized",
            "--disable-notifications",
            "--headless",
            "--disable-gpu",
            "--no-sandbox"
        ]
    }
}

TIMEOUTS = {
    'implicit': 10,
    'explicit': 10,
    'page_load': 30
}

def pytest_addoption(parser):
    parser.addoption("--id", action="store", help="store id in format XXX/XXX")
    parser.addoption("--noreport", action="store_true", help="disable HTML report generation")

@pytest.fixture(scope="session")
def logger(store_id):
    """Create logger for test run"""
    timestamp = datetime.now().strftime('%m%d_%H%M')
    logger_name = f"store_{store_id}" if store_id else "menu_test"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler(f"logs/{logger_name}_{timestamp}.log")
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    
    return logger

@pytest.fixture(scope="session")
def store_id(request):
    return request.config.getoption("--id")

@pytest.fixture
def driver(request, logger):
    browser = 'chrome'  # default browser
    
    if request.node.get_closest_marker('firefox'):
        browser = 'firefox'
    elif request.node.get_closest_marker('edge'):
        browser = 'edge'
    
    try:
        if browser == 'chrome':
            options = ChromeOptions()
            for option in BROWSER_OPTIONS['chrome']['default']:
                options.add_argument(option)
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            
        elif browser == 'firefox':
            options = FirefoxOptions()
            for option in BROWSER_OPTIONS['firefox']['default']:
                options.add_argument(option)
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
            
        elif browser == 'edge':
            options = EdgeOptions()
            for option in BROWSER_OPTIONS['edge']['default']:
                options.add_argument(option)
            driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=options)
        
        driver.implicitly_wait(TIMEOUTS['implicit'])
        driver.set_page_load_timeout(TIMEOUTS['page_load'])
        
        logger.info(f"Started {browser} browser")
        yield driver
        logger.info(f"Closing {browser} browser")
        driver.quit()
        
    except Exception as e:
        logger.error(f"Failed to create {browser} driver: {str(e)}")
        raise

@pytest.fixture
def sim_type(store_id, logger):
    """Determine simulation type based on store ID"""
    if store_id:
        with open('src/data/sim1_stores.csv') as f:
            if store_id in f.read():
                logger.info(f"Store {store_id} identified as sim1")
                return 'sim1'
        with open('src/data/sim2_stores.csv') as f:
            if store_id in f.read():
                logger.info(f"Store {store_id} identified as sim2")
                return 'sim2'
        logger.error(f"Store {store_id} not found in either simulation")
        raise ValueError(f"Store {store_id} not found in either simulation")