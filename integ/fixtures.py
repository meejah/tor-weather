from os.path import join, split
from subprocess import Popen, call
import pytest
from selenium.webdriver import Firefox
from fabric.api import cd, local

@pytest.fixture(scope="module")
def driver(request):
    '''
    Launches a Selenium instance.
    '''
    driver = Firefox()
    if True:
        request.addfinalizer(lambda: driver.quit())
    driver.implicitly_wait(1.0)  # seconds to wait for elements to appear
    return driver


@pytest.fixture(scope="module")
def onionoo(request):
    '''
    Runs the fake OnionOO server on the Vagrant VM; this just servs
    pre-canned data for /summary and /details.
    '''
    fakeoo = Popen(
        ['vagrant', 'ssh', '-c',
         'sudo twistd --pidfile=/tmp/oo.pid cyclone /home/weather/opt/current/vagrant/fake-onionoo.py'],
        cwd=join(split(__file__)[0], '..')
    )
    def terminate():
        call(['vagrant', 'ssh', '-c', 'sudo kill `cat /tmp/oo.pid`'])
    request.addfinalizer(terminate)


@pytest.fixture
def clean_data():
    '''
    Clears all the databases and deletes any accumulated confirmation emails.
    '''
    with cd('..'):
        local('vagrant ssh -c "sudo su www-data -c \'cd /home/weather/opt/current/weather && python ./manage.py clearmodels\'"')
    local('rm -f ../vagrant-emails/*')
    local('mkdir -p ../vagrant-emails')
