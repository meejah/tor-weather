import pytest
import sys

def test_register(driver):
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

#    assert(driver.
