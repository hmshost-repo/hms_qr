from src.pages.base_page import BasePage
from conftest import BASE_URL

class MenuPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_store(self, store_id):
        """Navigate to specific store menu"""
        url = f"{BASE_URL}/{store_id}"
        self.driver.get(url) 