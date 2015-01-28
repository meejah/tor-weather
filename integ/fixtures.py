import pytest
from selenium.webdriver import Firefox
from fabric.api import cd, local

@pytest.fixture(scope="module")
def driver(request, quit=True):
    """
    """
    driver = Firefox()
    if quit:
        request.addfinalizer(lambda: driver.quit())
    driver.implicitly_wait(1.0)  # seconds to wait for elements to appear
    return driver

@pytest.fixture
def clean_data():
    '''
    Clears all the databases and deletes any accumulated confirmation emails.
    '''
    with cd('..'):
        local('vagrant ssh -c "sudo su www-data -c \'cd /home/weather/opt/current/weather && python ./manage.py clearmodels\'"')
    local('rm -f ../vagrant-emails/*')
    local('mkdir -p ../vagrant-emails')
