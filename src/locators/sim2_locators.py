# Locators for simulation 2
from selenium.webdriver.common.by import By

class CommonLocators:
    CLOSE_POPUP_BUTTON = (By.CSS_SELECTOR, 'button#CookiePrefencesModalButton')

class MenuCategories:
    BREAKFAST = (By.XPATH, "//h1[contains(.,'Breakfast')]")
    SMASH_BURGER = (By.XPATH, "//h1[contains(.,'Smash Burger®')]")
    FRESH_SALADS = (By.XPATH, "//h1[contains(.,'Fresh Salads')]")
    FRIES = (By.XPATH, "//h1[contains(.,'Fries and Sides')]")
    NON_ALCOHOLIC = (By.XPATH, "//h1[contains(.,'Non-Alcoholic Beverages')]")

class PriceLocators:
    ITEM_PRICE_BY_NAME = (By.XPATH, "//h3[contains(text(),'{}')]/..//p[contains(@class,'palette-neutral100-color typography-text-p2')]")
    ITEM_CONTAINER = (By.XPATH, "//div[contains(@class,'menu-item')]")
    ITEM_NAME = (By.XPATH, ".//h3")
    ITEM_PRICE = (By.XPATH, ".//p[contains(@class,'palette-neutral100-color typography-text-p2')]")
    CATEGORY_CONTAINER = (By.XPATH, "//div[contains(@class,'category-section')]")