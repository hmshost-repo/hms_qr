from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import logging


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

    def get_text(self, locator, name=None):
        """Get text with multiple retry strategies"""
        logging.info(f"Attempting to get text from element: {name if name else locator}")
        try:
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

    def is_element_displayed(self, locator, timeout=5):
        """Check if element is displayed"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except TimeoutException:
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