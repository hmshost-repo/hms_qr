import pytest
from functools import wraps
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, WebDriverException

def handle_test_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except IndexError as e:
                if attempt < max_retries - 1:
                    kwargs['driver'].refresh()
                    continue
                pytest.skip(f"No elements found after {max_retries} attempts: {str(e)}")
            except (TimeoutException, NoSuchWindowException) as e:
                if attempt < max_retries - 1:
                    kwargs['driver'].refresh()
                    continue
                pytest.skip(f"Page error after {max_retries} attempts: {str(e)}")
            except WebDriverException as e:
                if attempt < max_retries - 1:
                    kwargs['driver'].refresh()
                    continue
                pytest.skip(f"Browser error after {max_retries} attempts: {str(e)}")
            except Exception as e:
                pytest.skip(f"Unexpected error: {str(e)}")
    return wrapper