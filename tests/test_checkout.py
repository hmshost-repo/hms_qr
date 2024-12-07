import random

import pytest
from src.pages.store.menu_page import MenuPage
from src.locators.store_locators import (
    MenuCategories,
    CustomizationLocators,
    AppetizerItems
)
from src.utils.config_reader import read_store_data

def get_all_store_ids():
    stores = read_store_data('src/data/stores.csv')

    return stores

@pytest.mark.checkout
@pytest.mark.parametrize('store_id', get_all_store_ids())
def test_select_bleu_cheese(driver, store_id):
    sauce_options = {
        CustomizationLocators.BLEU_CHEESE_CHECKBOX: CustomizationLocators.BLEU_CHEESE_CHECKED,
        CustomizationLocators.HOUSE_MADE_RANCH_CHECKBOX: CustomizationLocators.HOUSE_MADE_RANCH_CHECKED
    }
    checkbox, checked_state = random.choice(list(sauce_options.items()))
    
    menu_page = MenuPage(driver)
    menu_page.navigate_to_store(store_id)
    menu_page.navigate_to_category(MenuCategories.APPETIZERS)
    menu_page.navigate_to_category(AppetizerItems.BONELESS_HONEY_CHIPOTLE)
    menu_page.click(checkbox)
    assert menu_page.is_element_displayed(checked_state), "Sauce option was not selected"