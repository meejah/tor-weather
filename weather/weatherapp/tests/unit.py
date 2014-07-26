from types import StringType, TupleType

from django.core import mail
from django.test import TestCase

from .. import emails

TEST_STR = "test"


class GetRouterNameTests(TestCase):
    """Tests emails._get_router_name()"""
    def setUp(self):
        self.func_kwargs = {
            "fingerprint": TEST_STR,
            "name": TEST_STR,
        }

    def test_fingerprint_arg_undefined(self):
        del self.func_kwargs["fingerprint"]
        self.assertRaises(TypeError, emails._get_router_name, **self.func_kwargs)

    def test_name_arg_undefined(self):
        del self.func_kwargs["name"]
        self.assertRaises(TypeError, emails._get_router_name, **self.func_kwargs)

    def test_name_branch(self):
        val0 = emails._get_router_name(**self.func_kwargs)
        self.assertEqual(type(val0), StringType)

        self.func_kwargs["name"] = "Unnamed"
        val1 = emails._get_router_name(**self.func_kwargs)
        self.assertEqual(type(val1), StringType)

        self.assertNotEqual(val0, val1)


class AddGenericFooterTests(TestCase):
    """Tests emails._add_generic_footer()"""
    def setUp(self):
        self.func_kwargs = {
            "msg": TEST_STR,
            "pref_auth": TEST_STR,
            "unsubs_auth": TEST_STR,
        }

    def test_msg_arg_undefined(self):
        del self.func_kwargs["msg"]
        self.assertRaises(
            TypeError, emails._add_generic_footer, **self.func_kwargs)

    def test_unsubs_auth_arg_underfined(self):
        del self.func_kwargs["unsubs_auth"]
        self.assertRaises(
            TypeError, emails._add_generic_footer, **self.func_kwargs)

    def test_pref_auth_arg_undefined(self):
        del self.func_kwargs["pref_auth"]
        self.assertRaises(
            TypeError, emails._add_generic_footer, **self.func_kwargs)

    def test_ok(self):
        self.assertEqual(
            type(emails._add_generic_footer(**self.func_kwargs)), StringType)


class SendConfirmationTests(TestCase):
    """Tests emails.send_confirmation()"""
    def setUp(self):
        self.func_kwargs = {
            "confirm_auth": TEST_STR,
            "fingerprint": TEST_STR,
            "name": TEST_STR,
            "recipient": TEST_STR,
        }

    def test_recipient_arg_undefined(self):
        del self.func_kwargs["recipient"]
        self.assertRaises(
            TypeError, emails.send_confirmation, **self.func_kwargs)

    def test_fingerprint_arg_undefined(self):
        del self.func_kwargs["fingerprint"]
        self.assertRaises(
            TypeError, emails.send_confirmation, **self.func_kwargs)

    def test_name_arg_undefined(self):
        del self.func_kwargs["name"]
        self.assertRaises(
            TypeError, emails.send_confirmation, **self.func_kwargs)

    def test_confirm_auth_arg_undefined(self):
        del self.func_kwargs["confirm_auth"]
        self.assertRaises(
            TypeError, emails.send_confirmation, **self.func_kwargs)

    def test_ok(self):
        emails.send_confirmation(**self.func_kwargs)
        self.assertEqual(len(mail.outbox), 1)


class SendConfirmedTests(TestCase):
    """Tests emails.send_confirmed()"""
    def setUp(self):
        self.func_kwargs = {
            "fingerprint": TEST_STR,
            "name": TEST_STR,
            "pref_auth": TEST_STR,
            "recipient": TEST_STR,
            "unsubs_auth": TEST_STR,
        }

    def test_recipient_arg_undefined(self):
        del self.func_kwargs["recipient"]
        self.assertRaises(TypeError, emails.send_confirmed, **self.func_kwargs)

    def test_fingerprint_arg_undefined(self):
        del self.func_kwargs["fingerprint"]
        self.assertRaises(TypeError, emails.send_confirmed, **self.func_kwargs)

    def test_name_arg_undefined(self):
        del self.func_kwargs["name"]
        self.assertRaises(TypeError, emails.send_confirmed, **self.func_kwargs)

    def test_unsubs_auth_arg_undefined(self):
        del self.func_kwargs["unsubs_auth"]
        self.assertRaises(TypeError, emails.send_confirmed, **self.func_kwargs)

    def test_pref_auth_arg_undefined(self):
        del self.func_kwargs["pref_auth"]
        self.assertRaises(TypeError, emails.send_confirmed, **self.func_kwargs)

    def test_ok(self):
        emails.send_confirmed(**self.func_kwargs)
        self.assertEqual(len(mail.outbox), 1)


class BandwidthTupleTests(TestCase):
    """Tests emails.bandwidth_tuple()"""
    def setUp(self):
        self.func_kwargs = {
            "fingerprint": TEST_STR,
            "name": TEST_STR,
            "observed": 0,
            "pref_auth": TEST_STR,
            "recipient": TEST_STR,
            "threshold": 0,
            "unsubs_auth": TEST_STR,
        }

    def test_recipient_arg_undefined(self):
        del self.func_kwargs["recipient"]
        self.assertRaises(TypeError, emails.bandwidth_tuple, **self.func_kwargs)

    def test_fingerprint_arg_undefined(self):
        del self.func_kwargs["fingerprint"]
        self.assertRaises(TypeError, emails.bandwidth_tuple, **self.func_kwargs)

    def test_name_arg_undefined(self):
        del self.func_kwargs["name"]
        self.assertRaises(TypeError, emails.bandwidth_tuple, **self.func_kwargs)

    def test_observed_arg_undefined(self):
        del self.func_kwargs["observed"]
        self.assertRaises(TypeError, emails.bandwidth_tuple, **self.func_kwargs)

    def test_threshold_arg_undefined(self):
        del self.func_kwargs["threshold"]
        self.assertRaises(TypeError, emails.bandwidth_tuple, **self.func_kwargs)

    def test_unsubs_auth_arg_undefined(self):
        del self.func_kwargs["unsubs_auth"]
        self.assertRaises(TypeError, emails.bandwidth_tuple, **self.func_kwargs)

    def test_pref_auth_arg_undefined(self):
        del self.func_kwargs["pref_auth"]
        self.assertRaises(TypeError, emails.bandwidth_tuple, **self.func_kwargs)

    def test_ok(self):
        val = emails.bandwidth_tuple(**self.func_kwargs)
        self.assertEqual(len(val), 4)
        self.assertEqual(type(val), TupleType)


class NodeDownTupleTests(TestCase):
    """Tests emails.node_down_tuple()"""
    def setUp(self):
        self.func_kwargs = {
            "fingerprint": TEST_STR,
            "grace_pd": 0,
            "name": TEST_STR,
            "pref_auth": TEST_STR,
            "recipient": TEST_STR,
            "unsubs_auth": TEST_STR,
        }

    def test_recipient_arg_undefined(self):
        del self.func_kwargs["recipient"]
        self.assertRaises(TypeError, emails.node_down_tuple, **self.func_kwargs)

    def test_fingerprint_arg_undefined(self):
        del self.func_kwargs["fingerprint"]
        self.assertRaises(TypeError, emails.node_down_tuple, **self.func_kwargs)

    def test_name_arg_undefined(self):
        del self.func_kwargs["name"]
        self.assertRaises(TypeError, emails.node_down_tuple, **self.func_kwargs)

    def test_grace_pd_arg_undefined(self):
        del self.func_kwargs["grace_pd"]
        self.assertRaises(TypeError, emails.node_down_tuple, **self.func_kwargs)

    def test_unsubs_auth_arg_undefined(self):
        del self.func_kwargs["unsubs_auth"]
        self.assertRaises(TypeError, emails.node_down_tuple, **self.func_kwargs)

    def test_pref_auth_arg_undefined(self):
        del self.func_kwargs["pref_auth"]
        self.assertRaises(TypeError, emails.node_down_tuple, **self.func_kwargs)

    def test_ok(self):
        """Returns a tuple of four items."""
        val = emails.node_down_tuple(**self.func_kwargs)
        self.assertEqual(len(val), 4)
        self.assertEqual(type(val), TupleType)


class TShirtTupleTests(TestCase):
    """Tests emails.t_shirt_tuple()"""
    def setUp(self):
        self.func_kwargs = {
            "avg_bandwidth": 0,
            "fingerprint": TEST_STR,
            "hours_since_triggered": 0,
            "is_exit": True,
            "name": TEST_STR,
            "pref_auth": TEST_STR,
            "recipient": TEST_STR,
            "unsubs_auth": TEST_STR,
        }

    def test_recipient_arg_undefined(self):
        del self.func_kwargs["recipient"]
        self.assertRaises(TypeError, emails.t_shirt_tuple, **self.func_kwargs)

    def test_fingerprint_arg_undefined(self):
        del self.func_kwargs["fingerprint"]
        self.assertRaises(TypeError, emails.t_shirt_tuple, **self.func_kwargs)

    def test_name_arg_undefined(self):
        del self.func_kwargs["name"]
        self.assertRaises(TypeError, emails.t_shirt_tuple, **self.func_kwargs)

    def test_avg_bandwidth_undefined(self):
        del self.func_kwargs["avg_bandwidth"]
        self.assertRaises(TypeError, emails.t_shirt_tuple, **self.func_kwargs)

    def test_hours_since_triggered_arg_undefined(self):
        del self.func_kwargs["hours_since_triggered"]
        self.assertRaises(TypeError, emails.t_shirt_tuple, **self.func_kwargs)

    def test_is_exit_arg_undefined(self):
        del self.func_kwargs["is_exit"]
        self.assertRaises(TypeError, emails.t_shirt_tuple, **self.func_kwargs)

    def test_is_exit_branch(self):
        val0 = emails.t_shirt_tuple(**self.func_kwargs)
        self.assertEqual(type(val0), TupleType)

        self.func_kwargs["is_exit"] = False
        val1 = emails.t_shirt_tuple(**self.func_kwargs)
        self.assertEqual(type(val1), TupleType)

        self.assertNotEqual(val0, val1)

    def test_unsubs_auth_arg_undefined(self):
        del self.func_kwargs["unsubs_auth"]
        self.assertRaises(TypeError, emails.t_shirt_tuple, **self.func_kwargs)

    def test_pref_auth_arg_undefined(self):
        del self.func_kwargs["pref_auth"]
        self.assertRaises(TypeError, emails.t_shirt_tuple, **self.func_kwargs)

    def test_ok(self):
        val = emails.t_shirt_tuple(**self.func_kwargs)
        self.assertEqual(len(val), 4)
        self.assertEqual(type(val), TupleType)


class WelcomeTupleTests(TestCase):
    """Tests emails.welcome_tuple()"""
    def setUp(self):
        self.func_kwargs = {
            "fingerprint": TEST_STR,
            "exit": True,
            "name": TEST_STR,
            "recipient": TEST_STR,
        }

    def test_recipient_arg_undefined(self):
        del self.func_kwargs["recipient"]
        self.assertRaises(TypeError, emails.welcome_tuple, **self.func_kwargs)

    def test_fingerprint_arg_undefined(self):
        del self.func_kwargs["fingerprint"]
        self.assertRaises(TypeError, emails.welcome_tuple, **self.func_kwargs)

    def test_name_arg_undefined(self):
        del self.func_kwargs["name"]
        self.assertRaises(TypeError, emails.welcome_tuple, **self.func_kwargs)

    def test_exit_arg_undefined(self):
        del self.func_kwargs["exit"]
        self.assertRaises(TypeError, emails.welcome_tuple, **self.func_kwargs)

    def test_ok(self):
        val = emails.welcome_tuple(**self.func_kwargs)
        self.assertEqual(len(val), 4)
        self.assertEqual(type(val), TupleType)


class VersionTupleTests(TestCase):
    """Tests email.version_tuple()"""
    def setUp(self):
        self.func_kwargs = {
            "fingerprint": TEST_STR,
            "name": TEST_STR,
            "pref_auth": TEST_STR,
            "recipient": TEST_STR,
            "unsubs_auth": TEST_STR,
            "version_type": TEST_STR,
        }

    def test_recipient_arg_undefined(self):
        del self.func_kwargs["recipient"]
        self.assertRaises(TypeError, emails.version_tuple, **self.func_kwargs)

    def test_fingerprint_arg_undefined(self):
        del self.func_kwargs["fingerprint"]
        self.assertRaises(TypeError, emails.version_tuple, **self.func_kwargs)

    def test_name_arg_undefined(self):
        del self.func_kwargs["name"]
        self.assertRaises(TypeError, emails.version_tuple, **self.func_kwargs)

    def test_version_type_arg_undefined(self):
        del self.func_kwargs["version_type"]
        self.assertRaises(TypeError, emails.version_tuple, **self.func_kwargs)

    def test_unsubs_auth_arg_undefined(self):
        del self.func_kwargs["unsubs_auth"]
        self.assertRaises(TypeError, emails.version_tuple, **self.func_kwargs)

    def test_pref_auth_arg_undefined(self):
        del self.func_kwargs["pref_auth"]
        self.assertRaises(TypeError, emails.version_tuple, **self.func_kwargs)

    def test_ok(self):
        val = emails.version_tuple(**self.func_kwargs)
        self.assertEqual(len(val), 4)
        self.assertEqual(type(val), TupleType)
