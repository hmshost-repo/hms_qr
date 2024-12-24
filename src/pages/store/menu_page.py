from conftest import BASE_URL
from src.pages.base_page import BasePage
from src.locators.store_locators import (
    PriceLocators,
    MenuCategories,
    ModifierLocators,
    CommonLocators
)
import random
import logging
import pytest


class MenuPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def select_random_item(self):
        main_categories = self.get_elements(MenuCategories.ALL_CATEGORIES)
        random_category = random.choice(main_categories)
        self.click(random_category)
        while True:
            try:
                clickable_elements = self.get_elements(
                    MenuCategories.ALL_SUB_CATEGORIES,
                    MenuCategories.ALTERNATIVE_CATEGORIES
                )
                if not clickable_elements:
                    clickable_elements = self.get_elements(ModifierLocators.MENU_ITEMS)

                if clickable_elements:
                    random_element = random.choice(clickable_elements)
                    self.click(random_element)
                else:
                    self.driver.back()
                if self.is_element_displayed(ModifierLocators.ADD_TO_CART):
                    return True
            except Exception as e:
                self.logger.error(f"Error during navigation: {str(e)}")
                self.driver.back()
                continue


    def check_all_prices(self):
        price_to_check = "86.86"
        invalid_prices = {}
        processed_categories = set()
        errors_found = False

        initial_categories = [
            cat.text for cat in self.get_elements(MenuCategories.VISIBLE_SUBCATEGORIES)
            if cat.is_displayed()
        ]
        self.logger.info(f"Found {len(initial_categories)} main categories")

        def check_items_in_current_view(category_path=""):
            new_items = self.get_elements(PriceLocators.ITEM_NAME)
            if not new_items:
                return False

            self.logger.info(f"Found {len(new_items)} items in {category_path}")
            for item in new_items:
                new_item_name = None
                try:
                    new_item_name = item.text
                    self.click(item)
                    item_price = self.get_text(PriceLocators.INDIVIDUAL_PRICE)
                    self.logger.info(f"Checking {category_path} > {new_item_name}: {item_price}")

                    if item_price == price_to_check:
                        nonlocal errors_found
                        errors_found = True
                        item_path = category_path.replace(" > ", "/")
                        invalid_prices.setdefault(item_path, {})[new_item_name] = item_price
                        self.logger.error(f"Invalid price found: {item_path} > {new_item_name}: {item_price}")
                    self.driver.back()
                except Exception as e:
                    error_item = new_item_name if new_item_name else "unknown item"
                    self.logger.error(f"Error checking {error_item}: {str(e)}")
            return True

        def explore_category(main_category_name, depth=0, new_path=""):
            if main_category_name in processed_categories:
                self.logger.info(f"Already checked {main_category_name}, skipping...")
                return

            current_path = f"{new_path} > {main_category_name}" if new_path else main_category_name
            self.logger.info(f"\nExploring depth {depth}: {current_path}")

            try:
                category_locator = MenuCategories.CATEGORY_BY_NAME(main_category_name)
                self.click(category_locator)
                processed_categories.add(main_category_name)

                if check_items_in_current_view(current_path):
                    self.driver.back()
                    return

                subcategories = [
                    i.text for i in self.get_elements(MenuCategories.VISIBLE_SUBCATEGORIES)
                    if i.is_displayed() and i.text not in processed_categories
                ]

                if subcategories:
                    self.logger.info(f"Found subcategories in {current_path}: {subcategories}")
                    for i in subcategories:
                        explore_category(i, depth + 1, current_path)
                self.driver.back()
            except Exception as e:
                self.logger.error(f"Error exploring {current_path}: {str(e)}")
                for _ in range(depth + 1):
                    try:
                        self.driver.back()
                    except:
                        pass

        for category_name in initial_categories:
            explore_category(category_name)

        if errors_found:
            error_message = "\nInvalid prices found:\n"
            for path, items in invalid_prices.items():
                error_message += f"\nCategory: {path}"
                for item_name, price in items.items():
                    error_message += f"\n  - {item_name}: {price}"
            raise AssertionError(error_message)

        return invalid_prices

    def navigate_to_store(self, store_id):
        url = f"{BASE_URL}/{store_id}"
        self.driver.get(url)
        try:
            self.click(CommonLocators.CLOSE_POPUP_BUTTON)
            self.click(CommonLocators.CLOSE_AD_BUTTON)
        except:
            pass
        if not self.is_element_displayed(ModifierLocators.COPYRIGHT_LOGO, timeout=10):
            self.logger.error(f"Store {store_id} page is not loading properly")
            pytest.skip(f"Store {store_id} is not accessible")