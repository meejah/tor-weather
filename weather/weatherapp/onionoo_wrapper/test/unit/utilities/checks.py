"""
Unit tests for the wrapper's utilities.checks module
"""

import unittest
import json
from onionoo_wrapper.utilities import *
from onionoo_wrapper.objects import *


class TestChecks(unittest.TestCase):
    """ Test case for the relay checks """

    def setup(self):
        details_doc = open('details_doc').read()
        self.relays = json.loads(details_doc)['relays']

    def test_stable(self):
        relay_obj = RelayDetails(self.relays[0])
        stable_check = checks.is_stable(relay_obj)
        self.assertTrue(stable_check)

        relay_obj = RelayDetails(self.relays[1])
        stable_check = checks.is_stable(relay_obj)
        self.assertFalse(stable_check)

    def test_hibernating(self):
        relay_obj = RelayDetails(self.relays[1])
        hibernating_check = checks.is_hibernating(relay_obj)
        self.assertFalse(hibernating_check)

        relay_obj = RelayDetails(self.relays[2])
        hibernating_check = checks.is_hibernating(relay_obj)
        self.assertTrue(hibernating_check)
        
    def test_exitport(self):
        relay_obj = RelayDetails(self.relays[0])
        exit_check = checks.check_exitport(relay_obj)
        self.assertFalse(stable_check)
        
        relay_obj = RelayDetails(self.relays[1])
        exit_check = checks.check_exitport(relay_obj)
        self.assertFalse(stable_check)

if __name__ == '__main__':
    unittest.main()
