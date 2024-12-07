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
        skip_texts = ['Alcoholic Beverages', 'Non-Alcoholic Beverages']
        
        try:
            self.driver.implicitly_wait(2)
            
            def find_category(name):
                return self.driver.find_element(By.XPATH, f"//h1[contains(text(), '{name}')]")
            
            # Get just category names first
            categories = [(cat.text) for cat in self.driver.find_elements(By.XPATH, "//h1[contains(@class,'category-title') or contains(@class,'title')]")
                         if cat.is_displayed()]
            print(f"Found {len(categories)} categories")
            
            for category_name in categories:
                try:
                    print(f"\nFound category: {category_name}")
                    
                    if any(skip in category_name for skip in skip_texts):
                        print(f"Skipping {category_name}")
                        continue
                    
                    # Find category element fresh each time
                    category = find_category(category_name)
                    category.click()
                    
                    # Get items with fresh references
                    items = self.driver.find_elements(*PriceLocators.ITEM_NAME)
                    print(f"Found {len(items)} items in {category_name}")
                    
                    # Store item references before clicking
                    item_elements = [(item.text, item) for item in items]
                    
                    for item_name, item in item_elements:
                        try:
                            item.click()
                            
                            price = self.get_text(PriceLocators.INDIVIDUAL_PRICE)
                            print(f"Checking {item_name}: {price}")
                            
                            if price == "86.86":
                                if category_name not in invalid_prices:
                                    invalid_prices[category_name] = {}
                                invalid_prices[category_name][item_name] = price
                            
                            self.driver.back()
                            
                        except Exception as e:
                            print(f"Error checking {item_name}: {str(e)}")
                            continue
                    
                    # Go back to main menu
                    self.driver.back()
                    
                except Exception as e:
                    print(f"Error in category {category_name}: {str(e)}")
                    continue
                
        finally:
            self.driver.implicitly_wait(0)
            
        return invalid_prices