import re
import sys
from os import listdir
from os.path import join

import pytest
from fabric.api import local


@pytest.mark.incremental
class TestFullRegistration:
    def test_subscribe(self, driver, clean_data, onionoo):
        '''confirm we can subscribe'''
        # setup
        driver.get('https://weather.dev')

        # execute test
        e = driver.find_element_by_id("sign-up-link")
        e.click()
        # signup form
        email = "meejah@meejah.ca"
        fp = 'B69D45E2AC49A81E014425FF6E07C7435C9F89B0'

        driver.find_element_by_id("id_email_1").send_keys(email)
        driver.find_element_by_id("id_email_2").send_keys(email)
        driver.find_element_by_id("id_fingerprint").send_keys(fp)
        driver.find_element_by_id("id_node_down_grace_pd").clear()
        driver.find_element_by_id("id_node_down_grace_pd").send_keys("0")
        driver.find_element_by_id("submit-button").submit()

        assert('confirmation' in driver.title.lower())
        # we've now sent the email

    @pytest.fixture
    def confirmation_email(self):
        '''Collect our one (and only) email, returned as list-of-strings (each line)'''
        # find our email, from the vagrant box
        email_path = '../vagrant-emails'
        emails = listdir(email_path)
        assert len(emails) == 1
        with open(join(email_path, emails[0]), 'r') as f:
            return f.readlines()

    def test_confirmation_email(self, driver, confirmation_email):
        '''ensure we have the correct hash in the email somewhere'''
        assert(
            filter(
                lambda x: 'B69D 45E2 AC49 A81E 0144 25FF 6E07 C743 5C9F 89B0' in x,
                confirmation_email
            )
        )

    def test_confirmation_link(self, driver, confirmation_email, onionoo):
        '''confirm the confirmation link works'''
        matcher = re.compile(r'(https://weather\.dev/confirm/.*)')
        urls = filter(
            lambda x: x is not None,
            map(
                lambda x: matcher.search(x),
                confirmation_email
            )
        )

        # make sure we have just one, and visit it
        assert(len(urls) == 1)
        driver.get(urls[0].group(1))

        # did we get a "yay, you signed up!" page?
        assert('confirmation successful' in driver.title.lower())
        # ...and is there an additional email, now?
        assert(len(listdir('../vagrant-emails')) == 2)

    def test_unsubscribe(self, driver, onionoo):
        driver.find_element_by_id("unsubscribe-link").click()

        assert('subscription removed' in driver.title.lower())
