from src.pages.base_page import BasePage
from src.locators.sim1_locators import PriceLocators, MenuCategories
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
from conftest import BASE_URL
from src.locators.sim1_locators import CommonLocators

class MenuPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def navigate_to_store(self, store_id):
        """Navigate to store and handle initial popups"""
        self.driver.implicitly_wait(0)  # Set to 0 for initial load
        self.driver.set_page_load_timeout(5)  # Lower page load timeout
        
        try:
            url = f"{BASE_URL}/{store_id}"
            self.driver.get(url)
            
            # Handle popups immediately without any waits
            try:
                popup = self.driver.find_element(*CommonLocators.CLOSE_POPUP_BUTTON)
                if popup.is_displayed():
                    popup.click()
            except:
                pass
            
            try:
                ad = self.driver.find_element(*CommonLocators.CLOSE_AD_BUTTON)
                if ad.is_displayed():
                    ad.click()
            except:
                pass
                
        finally:
            self.driver.implicitly_wait(1)  # Set back to minimal wait
    
    def navigate_to_category(self, category_locator):
        """Navigate to specific category"""
        try:
            self.click(category_locator)
            return True
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Failed to navigate to category: {str(e)}")
            return False
    
    def get_item_price(self, item_name):
        """Get price for specific item with error handling"""
        try:
            price_locator = (By.XPATH, PriceLocators.ITEM_PRICE_BY_NAME[1].format(item_name))
            price = self.get_text(price_locator)
            self.logger.info(f"Found price {price} for item {item_name}")
            return price
        except (NoSuchElementException, TimeoutException):
            self.logger.error(f"Item not found: {item_name}")
            return None
    
    def get_all_prices_in_category(self):
        """Get all prices in current category with error handling"""
        try:
            prices = {}
            # Find all menu items in the current category
            containers = self.driver.find_elements(*PriceLocators.ITEM_CONTAINER)
            
            if not containers:
                self.logger.warning("No menu items found in current category")
                return prices
            
            # For each menu item, get its name and price
            for container in containers:
                try:
                    name = container.find_element(*PriceLocators.ITEM_NAME).text
                    price = container.find_element(*PriceLocators.ITEM_PRICE).text
                    prices[name] = price
                except NoSuchElementException as e:
                    self.logger.warning(f"Skipping incomplete menu item: {str(e)}")
                    continue
                    
            return prices
        except Exception as e:
            self.logger.error(f"Failed to get prices: {str(e)}")
            return {}
    
    def check_prices_across_categories(self):
        """Check prices across all menu categories"""
        invalid_prices = {}
        
        # Get all category buttons
        for category_name, category_locator in vars(MenuCategories).items():
            if not category_name.startswith('_'):  # Skip private attributes
                try:
                    # Navigate to category
                    if not self.navigate_to_category(category_locator):
                        continue
                    
                    # Get prices in this category
                    prices = self.get_all_prices_in_category()
                    
                    # Check for invalid prices
                    category_invalid = {
                        item: price for item, price in prices.items() 
                        if price == "$86.86"
                    }
                    
                    if category_invalid:
                        invalid_prices[category_name] = category_invalid
                        
                except Exception as e:
                    self.logger.error(f"Error checking category {category_name}: {str(e)}")
                    continue
        
        return invalid_prices
    
    def check_price(self, item_name, expected_price=None):
        """Check if item has specific price or is not $86.86"""
        price = self.get_item_price(item_name)
        if price is None:
            return False
        if expected_price:
            return price == expected_price
        return price != "$86.86"
    
