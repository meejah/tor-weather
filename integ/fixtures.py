import pytest
from selenium.webdriver import Firefox
from fabric.api import cd, local

@pytest.fixture(scope="module")
def driver(request, quit=False):
    """
    """
    driver = Firefox()
    if quit:
        request.addfinalizer(lambda: driver.quit())
    driver.implicitly_wait(1.0)  # seconds to wait for elements to appear
    return driver

@pytest.fixture
def clean_data():
    with cd('..'):
        print "clearmodels"
        local('vagrant ssh -c "sudo su www-data -c \'cd /home/weather/opt/current/weather && python ./manage.py clearmodels\'"')
    print "nuke emails"
    local('rm -f ../vagrant-emails/*')
