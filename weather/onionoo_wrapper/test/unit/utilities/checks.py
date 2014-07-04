"""
Unit tests for the wrapper's utilities.checks module
"""

import unittest
import json
from onionoo_wrapper.utilities import *
from onionoo_wrapper.objects import *


class FakeRelay:
    def __init__(self):
        self.hibernating = True
        self.flags = ["Fast", "Guard", "Running", "Stable", "V2Dir", "Valid"]
        self.exit_policy_summary = {"reject":["1-65535"]}
        self.observed_bandwidth = 30 * 1024


class FakeSubscription:
    def __init__(self):
        self.threshold = 25 * 1024


class TestChecks(unittest.TestCase):
    """ Test case for the relay checks """

    def setUp(self):
        self.relay = FakeRelay()

    def test_stable(self):
        stable_check = checks.is_stable(self.relay)
        self.assertTrue(stable_check)

        self.relay.flags.remove("Stable")
        stable_check = checks.is_stable(self.relay)
        self.assertFalse(stable_check)

    def test_hibernating(self):
        hibernating_check = checks.is_hibernating(self.relay)
        self.assertTrue(hibernating_check)

        self.relay.hibernating = False
        hibernating_check = checks.is_hibernating(self.relay)
        self.assertFalse(hibernating_check)

    def test_low_bandwidth(self):
        sub = FakeSubscription()

        low_bandwidth_check = checks.is_bandwidth_low(self.relay)
        self.assertFalse(low_bandwidth_check)
        low_bandwidth_check = checks.is_bandwidth_low(self.relay, sub)
        self.assertFalse(low_bandwidth_check)

        self.relay.observed_bandwidth = 5 * 1024
        low_bandwidth_check = checks.is_bandwidth_low(self.relay)
        self.assertTrue(low_bandwidth_check)
        low_bandwidth_check = checks.is_bandwidth_low(self.relay, sub)
        self.assertTrue(low_bandwidth_check)

        self.relay.observed_bandwidth = 22 * 1024
        low_bandwidth_check = checks.is_bandwidth_low(self.relay)
        self.assertFalse(low_bandwidth_check)
        low_bandwidth_check = checks.is_bandwidth_low(self.relay, sub)
        self.assertTrue(low_bandwidth_check)

    def test_exitport(self):
        exit_check = checks.check_exitport(self.relay)
        self.assertFalse(exit_check)

if __name__ == '__main__':
    unittest.main()
