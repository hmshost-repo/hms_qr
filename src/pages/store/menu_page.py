import time

from src.pages.base_page import BasePage
from src.locators.store_locators import PriceLocators, MenuCategories
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
from conftest import BASE_URL
from src.locators.store_locators import CommonLocators

class MenuPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def navigate_to_store(self, store_id):
        """Navigate to store and handle initial popups"""
        self.driver.implicitly_wait(0)
        self.driver.set_page_load_timeout(10)

        try:
            url = f"{BASE_URL}/{store_id}"
            self.driver.get(url)

            try:
                self.click(CommonLocators.CLOSE_POPUP_BUTTON)
            except:
                pass

            try:
                self.click(CommonLocators.CLOSE_AD_BUTTON)
            except:
                pass

        finally:
            self.driver.implicitly_wait(0)

    def navigate_to_category(self, category_locator):
        """Navigate to specific category"""
        try:
            self.click(category_locator)
            return True
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Failed to navigate to category: {str(e)}")
            return False

    def check_all_prices(self):
        """Check prices across all menu categories"""
        invalid_prices = {}
        checked_categories = set()  # Keep track of checked categories
        
        def check_items_in_current_view(category_path=""):
            """Check items in current view, returns True if found items"""
            items = self.driver.find_elements(*PriceLocators.ITEM_NAME)
            if items:
                print(f"Found {len(items)} items in {category_path}")
                
                for item in items:
                    try:
                        item_name = item.text
                        item.click()
                        
                        price = self.get_text(PriceLocators.INDIVIDUAL_PRICE)
                        print(f"Checking {category_path} > {item_name}: {price}")
                        
                        if price == "86.86":
                            current_path = category_path.replace(" > ", "/")
                            if current_path not in invalid_prices:
                                invalid_prices[current_path] = {}
                            invalid_prices[current_path][item_name] = price
                        
                        self.driver.back()
                        
                    except Exception as e:
                        print(f"Error checking {item_name}: {str(e)}")
                        continue
                return True
            return False

        def explore_category(category_name, depth=0, path=""):
            """Recursively explore category and its subcategories"""
            if category_name in checked_categories:
                print(f"Already checked {category_name}, skipping...")
                return
            
            current_path = f"{path} > {category_name}" if path else category_name
            print(f"\nExploring depth {depth}: {current_path}")
            
            try:
                # Find and click category using exact match
                category = self.driver.find_element(By.XPATH, 
                    f"//h1[contains(@class,'category-title') or contains(@class,'title')][normalize-space(text())='{category_name}']")
                category.click()
                checked_categories.add(category_name)  # Mark as checked
                
                # First try to find items
                if check_items_in_current_view(current_path):
                    self.driver.back()
                    return
                
                # If no items, look for subcategories
                subcategories = [cat.text for cat in
                               self.driver.find_elements(By.XPATH, "//h1[contains(@class,'category-title') or contains(@class,'title')]")
                               if cat.is_displayed() and cat.text not in checked_categories]
                
                if subcategories:
                    print(f"Found subcategories in {current_path}: {subcategories}")
                    for subcat in subcategories:
                        explore_category(subcat, depth + 1, current_path)
                        
                self.driver.back()
                
            except Exception as e:
                print(f"Error exploring {current_path}: {str(e)}")
                # Try to get back to main menu
                for _ in range(depth + 1):
                    try:
                        self.driver.back()
                    except:
                        pass
        
        try:
            self.driver.implicitly_wait(2)
            
            # Get initial categories
            categories = [cat.text for cat in 
                         self.driver.find_elements(By.XPATH, "//h1[contains(@class,'category-title') or contains(@class,'title')]")
                         if cat.is_displayed()]
            print(f"Found {len(categories)} main categories")
            
            for category_name in categories:
                explore_category(category_name)
                
        finally:
            self.driver.implicitly_wait(0)
            
        return invalid_prices