import random
import logging
from src.pages.base_page import BasePage
from src.locators.store_locators import ModifierLocators
from selenium.webdriver.common.by import By


class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    # def handle_modifiers(self):

    #     print("\n=== MODIFIER SELECTION PROCESS ===")
    #
    #     # Step 1: Get all modifier sections
    #     all_sections = self.get_elements(ModifierLocators.MODIFIER_HEADER)
    #     if not all_sections:
    #         print("No modifier sections found")
    #         return
    #
    #     print(f"\nFound {len(all_sections)} modifier sections")
    #
    #     # Step 2: Handle Required Modifiers
    #     all_required_modifiers = self.get_elements(ModifierLocators.MODIFIER_REQUIRED)
    #     for section in all_required_modifiers:
    #         print(f'required - {section.text}')
    #         if len(all_required_modifiers) > 1:
    #             random_selection = random.choice(section)
    #             self.click(random_selection)
    #             print("chose and clicked")
    #         else:
    #             self.click(section)
    #             print("clicked")
    #
    #
    #     all_non_required_modifiers = self.get_elements(ModifierLocators.MODIFIER_OPTIONAL)
    #
    #     for section in all_non_required_modifiers:
    #         print(f'optional - {section.text}')
    #         # random_selection = random.choice(section)
    #         # self.click(random_selection)
    #         # print("clicked")

    # def handle_modifiers(self):

    #     print("\n=== MODIFIER SELECTION PROCESS ===")
    #
    #     # Step 1: Get all modifier sections
    #     all_sections = self.get_elements(ModifierLocators.MODIFIER_HEADER)
    #     if not all_sections:
    #         print("No modifier sections found")
    #         return
    #
    #     print(f"\nFound {len(all_sections)} modifier sections")
    #
    #     # Step 2: Handle Required Modifiers
    #     print("\n--- REQUIRED MODIFIERS ---")
    #     required_sections = self.get_elements(ModifierLocators.MODIFIER_REQUIRED)
    #     for section in required_sections:
    #         # Get section name
    #         section_name = section.text
    #         print(f"\nRequired Section: {section_name}")
    #
    #         # Find radio buttons for this section
    #         radio_options = section.find_elements(*ModifierLocators.RADIO_OPTIONS)
    #         if radio_options:
    #             # Select one random option
    #             selected_option = random.choice(radio_options)
    #             # Get the text before clicking
    #             option_text = selected_option.find_element(By.XPATH, "following-sibling::label").text
    #             # Click the option
    #             self.click(selected_option)
    #             print(f"Selected: {option_text}")
    #         else:
    #             print("No clickable options found")
    #
    #     # Step 3: Handle Optional Modifiers
    #     print("\n--- OPTIONAL MODIFIERS ---")
    #     optional_sections = [
    #         section for section in all_sections
    #         if not section.find_elements(*ModifierLocators.MODIFIER_REQUIRED)
    #     ]
    #
    #     for section in optional_sections:
    #         section_name = section.text
    #         print(f"\nOptional Section: {section_name}")
    #
    #         # Find checkbox options
    #         checkbox_options = section.find_elements(*ModifierLocators.CHECKBOX_OPTIONS)
    #         if checkbox_options:
    #             # Randomly decide whether to select any
    #             if random.choice([True, False]):
    #                 # Select 1-2 random options
    #                 num_to_select = random.randint(1, min(2, len(checkbox_options)))
    #                 selected_options = random.sample(checkbox_options, num_to_select)
    #
    #                 for option in selected_options:
    #                     option_text = option.find_element(By.XPATH, "following-sibling::label").text
    #                     self.click(option)
    #                     print(f"Selected: {option_text}")
    #             else:
    #                 print("Chose not to select any options")
    #         else:
    #             print("No clickable options found")
    #
    #     print("\n=== MODIFIER SELECTION COMPLETE ===")

    def handle_modifiers(self):
        """
        Handle required and optional modifiers
        """
        # Find all required modifier groups
        required_groups = self.get_elements(ModifierLocators.REQUIRED_MODIFIER_GROUP)
        print(f"\nFound {len(required_groups)} required modifier groups")

        # Handle each required group
        for group in required_groups:
            radio_options = group.find_elements(*ModifierLocators.RADIO_OPTIONS)
            print(f"Options in required group: {len(radio_options)}")

            if radio_options:
                selected_option = random.choice(radio_options)
                self.click(selected_option)
                print(f"Selected required option")
            else:
                print("No options found in this required group")

        optional_groups = self.get_elements(ModifierLocators.OPTIONAL_MODIFIER_GROUP)
        print(f"\nFound {len(optional_groups)} optional modifier groups")

        for group in optional_groups:
            # Skip Additional Instructions and Remove sections
            group_title = group.text.lower()
            if 'additional instructions' in group_title or 'remove' in group_title:
                continue

            checkbox_options = group.find_elements(*ModifierLocators.CHECKBOX_OPTIONS)
            print(f"Options in optional group: {len(checkbox_options)}")

            if checkbox_options and random.choice([True, False]):
                # Randomly select 1-2 options from this group
                num_to_select = random.randint(1, min(2, len(checkbox_options)))
                selected_options = random.sample(checkbox_options, num_to_select)
                for option in selected_options:
                    self.click(option)
                    print(f"Selected optional option")
            else:
                print("Skipped this optional group")

        print("\n=== MODIFIER SELECTION COMPLETE ===")
