from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import logging
from selenium.webdriver.remote.webelement import WebElement
from typing import Union, List, Tuple


logging.basicConfig(level=logging.INFO)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)


    def send_keys(self, locator, text, clear=True, name=None):
        """Send keys with multiple retry strategies"""
        logging.info(f"Attempting to send keys to element: {name if name else locator}")
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))

            # Regular
            try:
                if clear:
                    element.clear()
                element.send_keys(text)
                logging.info(f"Successfully sent keys using regular method: {name if name else locator}")
                return element
            except Exception as e:
                logging.info(f"Regular send_keys failed: {str(e)}")

            # JavaScript
            try:
                if clear:
                    self.driver.execute_script("arguments[0].value = '';", element)
                self.driver.execute_script(f"arguments[0].value = arguments[1];", element, text)
                logging.info(f"Successfully sent keys using JavaScript: {name if name else locator}")
                return element
            except Exception as e:
                logging.info(f"JavaScript send_keys failed: {str(e)}")

            # ActionChains
            try:
                actions = ActionChains(self.driver)
                if clear:
                    actions.click(element).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(
                        Keys.BACK_SPACE)
                actions.send_keys(text).perform()
                logging.info(f"Successfully sent keys using ActionChains: {name if name else locator}")
                return element
            except Exception as e:
                logging.error(f"All send_keys attempts failed: {str(e)}")
                raise

        except Exception as e:
            logging.error(f"Failed to interact with element {name if name else locator}: {str(e)}")
            raise

    def get_text(self, locator, name=None, element=None):
        """Get text with multiple retry strategies"""
        logging.info(f"Attempting to get text from element: {name if name else locator}")
        try:
            if element is None:
                element = self.wait.until(EC.presence_of_element_located(locator))

            # Regular text
            try:
                text = element.text
                if text:
                    logging.info(f"Successfully got text using regular method: {text}")
                    return text
            except Exception as e:
                logging.info(f"Regular text failed: {str(e)}")

            # textContent attribute
            try:
                text = element.get_attribute('textContent')
                if text:
                    logging.info(f"Successfully got text using textContent: {text}")
                    return text.strip()
            except Exception as e:
                logging.info(f"textContent failed: {str(e)}")

            # JavaScript innerText
            try:
                text = self.driver.execute_script("return arguments[0].innerText;", element)
                if text:
                    logging.info(f"Successfully got text using JavaScript: {text}")
                    return text.strip()
            except Exception as e:
                logging.error(f"All text retrieval attempts failed: {str(e)}")
                raise

        except Exception as e:
            logging.error(f"Failed to get text from element {name if name else locator}: {str(e)}")
            raise

    def is_element_displayed(self, locator, timeout=None):
        """Check if element is displayed"""
        try:
            # First try a quick find_element without wait
            elements = self.driver.find_elements(*locator)
            if elements and elements[0].is_displayed():
                return True

            # If not found immediately or not displayed, try short wait
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False

    def wait_for_url_contains(self, partial_url, timeout=10):
        """Wait for URL to contain specific text"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(partial_url)
            )
            logging.info(f"URL contains '{partial_url}'")
            return True
        except TimeoutException:
            logging.error(f"URL does not contain '{partial_url}' within {timeout} seconds")
            return False


    def click(self, locator, name=None):
        """Click element with multiple retry strategies"""
        logging.info(f"Attempting to move to and click element: {name if name else locator}")
        try:
            # Wait for element
            element = self.wait.until(EC.presence_of_element_located(locator))

            # Regular click
            try:
                element.click()
                logging.info(f"Successfully clicked element using regular click: {name if name else locator}")
                return element
            except Exception as e:
                logging.info(f"Regular click failed, trying alternative methods: {str(e)}")

            # JavaScript click
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.driver.execute_script("arguments[0].click();", element)
                logging.info(f"Successfully clicked element using JavaScript: {name if name else locator}")
                return element
            except Exception as e:
                logging.info(f"JavaScript click failed, trying ActionChains: {str(e)}")

            # ActionChains
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()
                logging.info(f"Successfully clicked element using ActionChains: {name if name else locator}")
                return element
            except Exception as e:
                logging.error(f"All click attempts failed for {name if name else locator}: {str(e)}")
                raise

        except Exception as e:
            logging.error(f"Failed to interact with element {name if name else locator}: {str(e)}")
            raise

    def get_elements(self, *locators):
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            if elements:
                return elements
        return []

    def wait_for_elements(self, locator, timeout=3):
        """Wait for elements to be present and return them"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def alt_click(self, target: Union[WebElement, Tuple[str, str]], name=None):
        """Click element with multiple retry strategies"""
        logging.info(f"Attempting to move to and click element: {name if name else target}")
        try:
            # Get the element based on target type
            if isinstance(target, tuple):
                element = self.wait.until(EC.presence_of_element_located(target))
            else:
                element = target

            # Regular click
            try:
                element.click()
                logging.info(f"Successfully clicked element using regular click: {name if name else target}")
                return element
            except Exception as e:
                logging.info(f"Regular click failed, trying alternative methods: {str(e)}")

            # JavaScript click
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.driver.execute_script("arguments[0].click();", element)
                logging.info(f"Successfully clicked element using JavaScript: {name if name else target}")
                return element
            except Exception as e:
                logging.info(f"JavaScript click failed, trying ActionChains: {str(e)}")

            # ActionChains
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()
                logging.info(f"Successfully clicked element using ActionChains: {name if name else target}")
                return element
            except Exception as e:
                logging.error(f"All click attempts failed for {name if name else target}: {str(e)}")
                raise

        except Exception as e:
            logging.error(f"Failed to interact with element {name if name else target}: {str(e)}")
            raise

    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(
            EC.visibility_of_element_located(locator)
        )


    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is present on the page
        """
        try:
            self.wait_for_element_visible(locator)
            return True
        except:
            return False

    def get_elements_alt(self, *locators: Tuple[str, str]) -> List[WebElement]:
        """
        Find all elements matching any of the provided locators
        """
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            if elements:
                return elements
        return []