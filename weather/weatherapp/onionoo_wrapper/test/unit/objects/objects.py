"""
Unit tests for the wrapper's onionoo objects
"""

import unittest
import requests
from onionoo_wrapper.objects import *


class TestExceptions(unittest.TestCase):
    """ Test case for checking exceptions """

    def setup(self):
        self.req = OnionooRequest()

    def test_invalid_document(self):
        with self.assertRaises(InvalidDocumentTypeError)
            self.req.get_response('invalid_document_type')

    def test_onionoo_error(self):
        with self.assertRaises(OnionooError)
            self.req.get_response('details', params={'typo':'relay'})


class TestRequest(unittest.TestCase):
    """ Test case for the OnionooRequest object """

    def setup(self):
        self.req = OnionooRequest()

    def test_case_sensitivity(self):
        resp_1 = self.req.get_response('details')
        resp_2 = self.req.get_response('Details')
        self.assertEqual(resp_1.document.doc, resp_2.document.doc)

    def test_with_parameters(self):
        # can check with pre-downloaded document
        resp_1 = self.req.get_response('details', params={'type':'relay', 'running':'true' })
        normal_request = requests.get('https://onionoo.torproject.org/details', params={'type':'relay','running':'true'})
        resp_2 = self.req.DOC_TYPES['details'](normal_request.json())
        self.assertEqual(resp_1.document.doc, resp_2.document.doc)

    def test_without_parameters(self):
        resp_1 = self.req.get_response('details')
        normal_request = requests.get('https://onionoo.torproject.org/details')
        resp_2 = self.req.DOC_TYPES['details'](normal_request.json())
        self.assertEqual(resp_1.document.doc, resp_2.document.doc)


class TestResponseType(unittest.TestCase):
    """ Test case for checking response document types """

    def setup(self):
        self.req = OnionooRequest()

    def test_summary_doc(self):
        resp = self.req.get_response('summary')
        self.assertEqual(type(resp.document), objects.Summary)

    def test_details_doc(self):
        resp = self.req.get_response('details')
        self.assertEqual(type(resp.document), objects.Details)

    def test_bandwidth_doc(self):
        resp = self.req.get_response('bandwidth')
        self.assertEqual(type(resp.document), objects.Bandwidth)

    def test_weights_doc(self):
        resp = self.req.get_response('weights')
        self.assertEqual(type(resp.document), objects.Weights)

    def test_clients_doc(self):
        resp = self.req.get_response('clients')
        self.assertEqual(type(resp.document), objects.Clients)

    def test_uptime_doc(self):
        resp = self.req.get_response('uptime')
        self.assertEqual(type(resp.document), objects.Uptime)

if __name__ == '__main__':
    unittest.main()
