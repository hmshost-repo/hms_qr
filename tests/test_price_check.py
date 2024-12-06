import pytest
from src.locators.sim1_locators import AppetizerItems, MenuCategories
from src.pages.sim1.menu_page import MenuPage

def test_appetizer_prices(driver, logger):
    menu_page = MenuPage(driver)
    
    # Navigate to Appetizers first
    menu_page.navigate_to_category(MenuCategories.APPETIZERS)
    
    # Use AppetizerItems constants instead of string
    price = menu_page.get_item_price(AppetizerItems.BONELESS_BUFFALO_WINGS[1])
    assert price is not None, "Item not found"
    assert price != "$86.86", f"Found invalid price {price} for Boneless Buffalo Wings"
    
    # Check all items in category
    prices = menu_page.get_all_prices_in_category()
    assert prices, "No items found in category"
    for item, price in prices.items():
        assert price != "$86.86", f"Found invalid price {price} for {item}"

def test_all_categories_prices(driver, logger):
    menu_page = MenuPage(driver)
    invalid_prices = menu_page.check_prices_across_categories()
    
    # If any invalid prices found, format error message
    if invalid_prices:
        error_msg = "\nInvalid prices found:\n"
        for category, items in invalid_prices.items():
            error_msg += f"\n{category}:\n"
            for item, price in items.items():
                error_msg += f"  - {item}: {price}\n"
        pytest.fail(error_msg) 