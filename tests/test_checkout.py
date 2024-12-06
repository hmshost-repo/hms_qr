"""Test module for checkout functionality."""

import pytest
from src.pages.sim1.menu_page import MenuPage
from src.locators.sim1_locators import (
    MenuCategories,
    CustomizationLocators,
    AppetizerItems
)
from src.utils.config_reader import read_store_data

def get_all_store_ids():
    sim1_stores = read_store_data('src/data/sim1_stores.csv')
    sim2_stores = read_store_data('src/data/sim2_stores.csv')
    return sim1_stores + sim2_stores

@pytest.mark.checkout
@pytest.mark.parametrize('store_id', get_all_store_ids())
def test_select_bleu_cheese(driver, store_id):
    """Test selecting bleu cheese option for boneless wings."""
    menu_page = MenuPage(driver)
    menu_page.navigate_to_store(store_id)
    menu_page.navigate_to_category(MenuCategories.APPETIZERS)
    menu_page.navigate_to_category(AppetizerItems.BONELESS_BUFFALO_WINGS)
    menu_page.click(CustomizationLocators.BLEU_CHEESE_CHECKBOX)
    assert menu_page.is_element_displayed(
        CustomizationLocators.BLEU_CHEESE_CHECKED
    ), "Bleu Cheese was not selected"