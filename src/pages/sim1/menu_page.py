from src.pages.base_page import BasePage
from src.locators.sim1_locators import PriceLocators, MenuCategories
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
from conftest import BASE_URL
from src.locators.sim1_locators import CommonLocators


def escape_quotes(text):
    if "'" in text:
        return f'"{text}"'
    return f"'{text}'"


class MenuPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def navigate_to_store(self, store_id):
        self.driver.set_page_load_timeout(3)  # Lower page load timeout
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
            self.driver.implicitly_wait(1)
    
    def navigate_to_category(self, category_locator):
        try:
            self.click(category_locator)
            return True
        except (NoSuchElementException, TimeoutException) as e:
            self.logger.error(f"Failed to navigate to category: {str(e)}")
            return False

    def check_all_prices(self):
        # Skip drink categories
        skip_categories = ['ALCOHOLIC', 'NON_ALCOHOLIC']
        invalid_items = []

        available_categories = {}
        for attr in dir(MenuCategories):
            if not attr.startswith('_') and attr not in skip_categories:
                category = getattr(MenuCategories, attr)
                try:
                    element = self.driver.find_element(*category)
                    if element.is_displayed():
                        available_categories[attr] = category
                except NoSuchElementException:
                    continue

        print(f"\nFound categories: {list(available_categories.keys())}")

        # Check each available category
        for category_name, category in available_categories.items():
            print(f"\nChecking category: {category_name}")

            # Go to category
            self.click(category)

            # Get all items in current category
            items = self.driver.find_elements(*PriceLocators.ITEM_NAME)

            # Check each item in category
            for item in items:
                item_name = ""
                try:
                    item_name = item.text
                    print(f"Checking item: {item_name}")

                    # Click on item with escaped special characters
                    xpath = f"//h3[contains(text(),{escape_quotes(item_name)})]"
                    self.click((By.XPATH, xpath))

                    # Try to get individual price using base_page method
                    try:
                        price = self.get_text(PriceLocators.INDIVIDUAL_PRICE, name=item_name)
                        print(f"Price: {price}")

                        if price == "86.86":
                            invalid_items.append(f"{category_name} - {item_name}\n")
                            print(f"Invalid price found: {price}")
                            print(invalid_items)
                    except:
                        print(f"No price found for {item_name}\n")

                    # Go back to category
                    self.driver.back()

                except Exception as e:
                    print(f"Error checking {item_name}: {str(e)}")
                    continue

            # Go back to main menu
            self.driver.back()
        return invalid_items
