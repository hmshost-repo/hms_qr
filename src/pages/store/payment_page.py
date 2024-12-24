import time

from src.pages.base_page import BasePage
from src.utils.credit_card import TEST_CARD
from src.locators.store_locators import PaymentPageLocators

class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def place_the_order(self):
        try:
            card_data = TEST_CARD
            self.send_keys(PaymentPageLocators.NAME_ON_CARD,card_data['fullname'])
            self.switch_to_frame(PaymentPageLocators.FRAME)
            self.send_keys(PaymentPageLocators.CARD_NUMBER, card_data['number'])
            self.send_keys(PaymentPageLocators.EXPIRATION_DATE, card_data['exp'])
            self.send_keys(PaymentPageLocators.SECURITY_CODE, card_data['cvv'])
            self.send_keys(PaymentPageLocators.POSTAL_CODE, card_data['zip'])
            self.switch_to_default_content()
            self.click(PaymentPageLocators.PAY_BUTTON)
            assert "Thanks" in PaymentPageLocators.SUCCESS_MESSAGE
        except:
            pass