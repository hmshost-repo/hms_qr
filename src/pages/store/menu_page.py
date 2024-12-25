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
from datetime import datetime
from pathlib import Path


class MenuPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.store_id = None
        self.screenshots_dir = Path("screenshots/invalid_prices")
        self.screenshots_dir.mkdir(exist_ok=True)

    def take_item_screenshot(self, store_id, item_name):
        timestamp = datetime.now().strftime('%H_%M')
        safe_store_id = store_id.replace('/', '_')
        safe_item_name = "".join(c for c in item_name if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{safe_store_id} {safe_item_name} - {timestamp}.png"
        filepath = self.screenshots_dir / filename
        self.driver.save_screenshot(str(filepath))
        self.logger.info(f"Screenshot saved: {filepath}")

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
        invalid_items = []
        price_to_check = "86.86"
        processed_categories = set()

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
            for i in new_items:
                new_item_name = None
                try:
                    new_item_name = i.text
                    self.click(i)
                    item_price = self.get_text(PriceLocators.INDIVIDUAL_PRICE)
                    self.logger.info(f"Checking {category_path} > {new_item_name}: {item_price}")

                    if item_price == price_to_check:
                        self.take_item_screenshot(self.store_id, new_item_name)
                        
                        invalid_items.append({
                            'category': category_path,
                            'name': new_item_name,
                            'price': item_price
                        })
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

        return invalid_items

    def navigate_to_store(self, store_id):
        self.store_id = store_id
        url = f"{BASE_URL}/{store_id}"
        self.driver.get(url)

        try:
            if self.is_element_displayed(CommonLocators.CLOSE_AD_BUTTON, timeout=3):
                self.click(CommonLocators.CLOSE_AD_BUTTON)

            if self.is_element_displayed(CommonLocators.CLOSE_POPUP_BUTTON, timeout=3):
                self.click(CommonLocators.CLOSE_POPUP_BUTTON)
        except:
            pass
        
        if not self.is_element_displayed(ModifierLocators.COPYRIGHT_LOGO, timeout=10):
            pytest.skip(f"Store {store_id} is not accessible")