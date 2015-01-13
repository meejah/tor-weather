import pytest
from selenium.webdriver import Firefox

@pytest.fixture
def driver(request, quit=True):
    """
    """
    driver = Firefox()
    if quit:
        request.addfinalizer(lambda: driver.quit())
    driver.implicitly_wait(1.0)  # seconds to wait for elements to appear
    return driver
