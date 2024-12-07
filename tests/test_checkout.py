import random
import time

import pytest
from src.pages.store.menu_page import MenuPage
from src.utils.config_reader import read_store_data

def get_all_store_ids():
    stores = read_store_data('src/data/stores.csv')
    return stores

@pytest.mark.checkout
@pytest.mark.parametrize('store_id', get_all_store_ids())
def test_random_item_checkout(driver, store_id):
    menu_page = MenuPage(driver)
    menu_page.navigate_to_store(store_id)
    menu_page.select_random_item()
    time.sleep(5)
