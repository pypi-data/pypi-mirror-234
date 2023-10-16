import unittest
from nemonet.runner.tool import SeleniumTool, WebdriverError

class RunnerToolTestCase(unittest.TestCase):

    def test_setup_driver(self):

        """ only tests if the method runs for all webdrivers """

        SeleniumTool.setup_driver(None)

        chrome_config = {
            "webdriver": "chrome",
            "webdriver_config": None
        }
        SeleniumTool.setup_driver(chrome_config)


    def test_setup_driver_raises_error(self):

        unsupported_config = {
            "webdriver": "unknown webdriver",
            "webdriver_config": None
        }
        with self.assertRaises(WebdriverError):
            SeleniumTool.setup_driver(unsupported_config)
