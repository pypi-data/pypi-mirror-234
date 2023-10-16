import unittest
from nemonet.runner.webdriver import ChromeTestDriver

class RunnerDriverTestCase(unittest.TestCase):

    def test_chrometestdriver_config_init(self):

        """ tests if ChromeTestDrivers can be correctly instantiated
            with a specific configuration """

        flag = ["dummy"]
        settings = {"dummy": "remote_settings"}
        config_full = {
            "headless" : True,
            "experimental_flags" : flag,
            "remote_settings" : settings
        }
        config_empty = {
            "headless": False,
            "experimental_flags": None,
            "remote_settings": None
        }

        c_full = ChromeTestDriver(config=config_full)

        msg = "ChromeTestDriver init with configuration issue for :"
        self.assertTrue(c_full.headless, msg=msg + "headless")
        self.assertEqual(c_full.experimental_flags, flag, msg=msg + "experimental flags")
        self.assertEqual(c_full.remote_settings, settings, msg=msg + "remote settings")

        c_empty = ChromeTestDriver(config=config_empty)
        self.assertFalse(c_empty.headless, msg=msg + "headless")
        self.assertEqual(c_empty.experimental_flags, [], msg=msg + "experimental flags")
        self.assertEqual(c_empty.remote_settings, {}, msg=msg + "experimental flags")