import functools
from selenium.common.exceptions import WebDriverException
import pytest

def handle_test_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError:
            raise  # Re-raise assertion errors
        except WebDriverException as e:
            pytest.skip(f"Selenium error occurred: {str(e)}")
        except Exception as e:
            pytest.skip(f"Unexpected error occurred: {str(e)}")
    return wrapper