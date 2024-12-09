import random
import logging
import time

from src.pages.base_page import BasePage
from src.locators.store_locators import ModifierLocators



class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def handle_modifiers(self):

        required_groups = self.get_elements(ModifierLocators.REQUIRED_MODIFIER_GROUP)
        for group in required_groups:
            radio_options = group.find_elements(*ModifierLocators.RADIO_OPTIONS)
            if radio_options:
                selected_option = random.choice(radio_options)
                self.click(selected_option)
        optional_groups = self.get_elements(ModifierLocators.OPTIONAL_MODIFIER_GROUP)

        for group in optional_groups:
            group_title = group.text.lower()
            if 'additional instructions' in group_title or 'remove' in group_title:
                continue
            checkbox_options = group.find_elements(*ModifierLocators.CHECKBOX_OPTIONS)
            if checkbox_options and random.choice([True, False]):
                num_to_select = random.randint(1, min(2, len(checkbox_options)))
                selected_options = random.sample(checkbox_options, num_to_select)
                for option in selected_options:
                    self.click(option)

    def add_to_cart(self):
        self.click(ModifierLocators.ADD_TO_CART)


    def go_to_cart(self):
        time.sleep(0.5)
        self.click(ModifierLocators.CART_BUTTON)

    def pay_now(self):
        self.click(ModifierLocators.PAY_NOW_BUTTON)