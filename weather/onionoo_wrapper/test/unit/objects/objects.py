"""
Unit tests for the wrapper's onionoo objects
"""

import unittest
import mock
import onionoo_wrapper.objects
from onionoo_wrapper.objects import *


class FakeResponse:
    def __init__(self, code):
        self.status_code = code
        self.headers = None
        self.reason = ""

    def json(self):
        return {'relays': [], 'bridges': []}


class TestExceptions(unittest.TestCase):
    """ Test case for checking exceptions """

    def setUp(self):
        self.req = OnionooRequest()

    def test_invalid_document(self):
        with self.assertRaises(InvalidDocumentTypeError):
            self.req.get_response('invalid_document_type')

    def test_invalid_parameter(self):
        with self.assertRaises(InvalidParameterError):
            self.req.get_response('details', params={'typo': 'relay'})

    @mock.patch('onionoo_wrapper.objects.requests')
    def test_onionoo_error(self, mock_requests):
        with self.assertRaises(OnionooError):
            mock_requests.get.return_value = FakeResponse(400)
            self.req.get_response('details', params={'type': 'node'})


class TestRequest(unittest.TestCase):
    """ Test case for the OnionooRequest object """

    def setUp(self):
        self.req = OnionooRequest()

    @mock.patch('onionoo_wrapper.objects.requests')
    def test_without_parameters(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        self.req.get_response('details')
        mock_requests.get.assert_called_with(
            self.req.ONIONOO_URL + 'details', params={})

    @mock.patch('onionoo_wrapper.objects.requests')
    def test_with_parameters(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        self.req.get_response(
            'details', params={'type': 'relay', 'running': 'true'})
        mock_requests.get.assert_called_with(
            self.req.ONIONOO_URL + 'details',
            params={'type': 'relay', 'running': 'true'})


class TestResponseType(unittest.TestCase):
    """ Test case for checking response document types """

    def setUp(self):
        self.req = OnionooRequest()

    @mock.patch('onionoo_wrapper.objects.requests')
    def test_summary_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.get_response('summary')
        self.assertEqual(type(resp.document), Summary)

    @mock.patch('onionoo_wrapper.objects.requests')
    def test_details_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.get_response('details')
        self.assertEqual(type(resp.document), Details)

    @mock.patch('onionoo_wrapper.objects.requests')
    def test_bandwidth_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.get_response('bandwidth')
        self.assertEqual(type(resp.document), Bandwidth)

    @mock.patch('onionoo_wrapper.objects.requests')
    def test_weights_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.get_response('weights')
        self.assertEqual(type(resp.document), Weights)

    @mock.patch('onionoo_wrapper.objects.requests')
    def test_clients_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.get_response('clients')
        self.assertEqual(type(resp.document), Clients)

    @mock.patch('onionoo_wrapper.objects.requests')
    def test_uptime_doc(self, mock_requests):
        mock_requests.get.return_value = FakeResponse(200)
        resp = self.req.get_response('uptime')
        self.assertEqual(type(resp.document), Uptime)

if __name__ == '__main__':
    unittest.main()
