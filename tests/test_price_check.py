import pytest
from src.pages.sim1.menu_page import MenuPage
from src.locators.sim1_locators import MenuCategories, AppetizerItems, PriceLocators
from src.utils.config_reader import read_store_data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

def get_all_store_ids():
    sim1_stores = read_store_data('src/data/sim1_stores.csv')
    sim2_stores = read_store_data('src/data/sim2_stores.csv')
    return sim1_stores + sim2_stores




@pytest.mark.price_check
@pytest.mark.parametrize('store_id', get_all_store_ids())
def test_check_prices_in_categories(driver, store_id):
    menu_page = MenuPage(driver)
    menu_page.navigate_to_store(store_id)
    invalid_items = menu_page.check_all_prices()
    assert not invalid_items, f"Found items with price $86.86: {invalid_items}"