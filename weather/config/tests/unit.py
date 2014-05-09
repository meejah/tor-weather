from django.test import TestCase

from config import url_helper


class TestGetConfirmUrl(TestCase):
    """Tests url_helper.get_confirm_url()"""
    def test_no_arg(self):
        self.assertRaises(TypeError, url_helper.get_confirm_url)

    def test_ok(self):
        val = url_helper.get_confirm_url("01234")
        self.assertEqual(val, "https://weather.torproject.org/confirm/01234/")


class TestGetConfirmPrefExt(TestCase):
    """Tests url_helper.get_confirm_pref_ext()"""
    def test_no_arg(self):
        self.assertRaises(TypeError, url_helper.get_confirm_pref_ext)

    def test_ok(self):
        val = url_helper.get_confirm_pref_ext("01234")
        self.assertEqual(val, "/confirm_pref/01234/")


class TestGetErrorExt(TestCase):
    """Tests url_helper.get_error_ext()"""
    def test_no_args(self):
        self.assertRaises(TypeError, url_helper.get_error_ext)

    def test_no_second_arg(self):
        self.assertRaises(TypeError, url_helper.get_error_ext, ("01234",))

    def test_ok(self):
        val = url_helper.get_error_ext("01234", "56789")
        self.assertEqual(val, "/error/01234/56789/")


class TestGetFingerprintInfoExt(TestCase):
    """Tests url_helper.get_fingerprint_info_ext()"""
    def test_no_arg(self):
        self.assertRaises(TypeError, url_helper.get_fingerprint_info_ext)

    def test_ok(self):
        val = url_helper.get_fingerprint_info_ext("01234")
        self.assertEqual(val, "/fingerprint_not_found/01234/")


class TestGetHomeExt(TestCase):
    """Tests url_helper.get_home_ext()"""
    def test_ok(self):
        val = url_helper.get_home_ext()
        self.assertEqual(val, "/")


class TestGetHomeUrl(TestCase):
    """Tests url_helper.get_home_url()"""
    def test_ok(self):
        val = url_helper.get_home_url()
        self.assertEqual(val, "https://weather.torproject.org/")


class TestGetPendingExt(TestCase):
    """Tests url_helper.get_pending_ext()"""
    def test_no_arg(self):
        self.assertRaises(TypeError, url_helper.get_pending_ext)

    def test_ok(self):
        val = url_helper.get_pending_ext("01234")
        self.assertEqual(val, "/pending/01234/")


class TestGetPreferencesUrl(TestCase):
    """Tests url_helper.get_preferences_url()"""
    def test_no_arg(self):
        self.assertRaises(TypeError, url_helper.get_preferences_url)

    def test_ok(self):
        val = url_helper.get_preferences_url("01234")
        self.assertEqual(val, "https://weather.torproject.org/preferences/01234/")


class TestGetPreferencesExt(TestCase):
    """Tests url_helper.get_preferences_ext()"""
    def test_no_arg(self):
        self.assertRaises(TypeError, url_helper.get_preferences_ext)

    def test_ok(self):
        val = url_helper.get_preferences_ext("01234")
        self.assertEqual(val, "/preferences/01234/")


class TestGetResendExt(TestCase):
    """Tests url_helper.get_resend_ext()"""
    def test_no_arg(self):
        self.assertRaises(TypeError, url_helper.get_resend_ext)

    def test_ok(self):
        val = url_helper.get_resend_ext("01234")
        self.assertEqual(val, "/resend_conf/01234/")


class TestGetSubscribeExt(TestCase):
    """Tests url_helper.get_subscribe_ext()"""
    def test_ok(self):
        val = url_helper.get_subscribe_ext()
        self.assertEqual(val, "/subscribe/")


class TestGetUnsubscribeUrl(TestCase):
    """Tests url_helper.get_unsubscribe_url()"""
    def test_no_arg(self):
        self.assertRaises(TypeError, url_helper.get_unsubscribe_url)

    def test_ok(self):
        val = url_helper.get_unsubscribe_url("01234")
        self.assertEqual(val, "https://weather.torproject.org/unsubscribe/01234/")


class TestGetDownloadUrl(TestCase):
    """Tests url_helper.get_download_url()"""
    def test_ok(self):
        val = url_helper.get_download_url()
        self.assertEqual(val, "https://www.torproject.org/easy-download.html")


class TestGetTShirtUrl(TestCase):
    """Tests url_helper.get_t_shirt_url()"""
    def test_ok(self):
        val = url_helper.get_t_shirt_url()
        self.assertEqual(
            val, "https://www.torproject.org/getinvolved/tshirt.html")
