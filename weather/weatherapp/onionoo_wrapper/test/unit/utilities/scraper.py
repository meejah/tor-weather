"""
Unit tests for the wrapper's utilities.scraper module
"""

import unittest
from onionoo_wrapper.utilities.scraper import *


class TestScraper(unittest.TestCase):
    """ Test case for the email-parser """

    def test_ok(self):
        class FakeRelay:
            def __init__(self):
                self.contact = "linux at perron-network dot com"

        relay = FakeRelay()
        email = deobfuscate_mail(relay)
        self.assertEqual(email, "linux@perron-network.com")

        relay.contact = "Elmo M\uFFFD\uFFFDntynen <elmo dot mantynen AT iki dot fi>"
        email = deobfuscate_mail(relay)
        self.assertEqual(email, "mantynen@iki.fi")

if __name__ == '__main__':
    unittest.main()
