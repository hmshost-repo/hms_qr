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


def escape_quotes(text):
    """Handle special characters in XPath"""
    if "'" in text:
        # If text contains single quotes, wrap it in double quotes
        return f'"{text}"'
    return f"'{text}'"

@pytest.mark.price_check
@pytest.mark.parametrize('store_id', get_all_store_ids())
def test_check_prices_in_categories(driver, store_id):
    menu_page = MenuPage(driver)
    menu_page.navigate_to_store(store_id)
    
    # Skip drink categories
    skip_categories = ['ALCOHOLIC', 'NON_ALCOHOLIC']
    invalid_items = []
    
    # First get available categories on the page
    available_categories = {}
    for attr in dir(MenuCategories):
        if not attr.startswith('_') and attr not in skip_categories:
            category = getattr(MenuCategories, attr)
            try:
                element = driver.find_element(*category)
                if element.is_displayed():
                    available_categories[attr] = category
            except NoSuchElementException:
                continue
    
    print(f"\nFound categories: {list(available_categories.keys())}")
    
    # Check each available category
    for category_name, category in available_categories.items():
        print(f"\nChecking category: {category_name}")
        
        # Go to category
        menu_page.click(category)
        
        # Get all items in current category
        items = driver.find_elements(*PriceLocators.ITEM_NAME)
        
        # Check each item in category
        for item in items:
            item_name = ""
            try:
                item_name = item.text
                print(f"Checking item: {item_name}")
                
                # Click on item with escaped special characters
                xpath = f"//h3[contains(text(),{escape_quotes(item_name)})]"
                menu_page.click((By.XPATH, xpath))
                
                # Try to get individual price using base_page method
                try:
                    price = menu_page.get_text(PriceLocators.INDIVIDUAL_PRICE, name=item_name)
                    print(f"Price: {price}")
                    
                    if price == "$86.86":
                        invalid_items.append(f"{category_name} - {item_name}")
                except:
                    print(f"No price found for {item_name}")
                
                # Go back to category
                driver.back()
                
            except Exception as e:
                print(f"Error checking {item_name}: {str(e)}")
                continue
        
        # Go back to main menu
        driver.back()
    
    # Assert no invalid prices were found
    assert not invalid_items, f"Found items with price $86.86: {invalid_items}"