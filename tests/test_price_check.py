import pytest
from src.pages.store.menu_page import MenuPage
from src.utils.config_reader import read_store_data


def get_all_store_ids():
    stores = read_store_data('src/data/stores.csv')
    return stores




@pytest.mark.price_check
@pytest.mark.parametrize('store_id', get_all_store_ids())
def test_check_prices_in_categories(driver, store_id):
    menu_page = MenuPage(driver)
    menu_page.navigate_to_store(store_id)
    invalid_items = menu_page.check_all_prices()
    assert not invalid_items, f"Found items with price $86.86: {invalid_items}"