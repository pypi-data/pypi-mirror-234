# Created by Jan Rummens at 12/01/2021
import unittest
import copy
import threading

from nemonet.runner.runner import Runner

import logging.config

logging.config.fileConfig(fname='../../vision_logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class RemoteTestCase(unittest.TestCase):

    """ Before running these tests, make sure Selenium Grid has been set up locally """

    def setUp(self) -> None:
        self.config = {
            "driver": {
                "tool": "selenium",
                "tool_config": {
                    "webdriver": "chrome",
                    "webdriver_config": {
                        "headless": True,
                        "experimental_flags": [
                            "same-site-by-default-cookies@2",
                            "cookies-without-same-site-must-be-secure@2"],
                        "remote_settings": None
                    }
                }
            },
            "screen_recording": {
                "enable": False
            }
        }

    def test_remote_chrome(self):
        # Before running this test, make sure Selenium Grid has been set up locally
        remote_config = copy.deepcopy(self.config)
        remote_settings = {"command_executor": "http://127.0.0.1:4444"}
        remote_config["driver"]["tool_config"]["webdriver_config"]["remote_settings"] = remote_settings
        remote_runner = Runner(config=remote_config)

        remote_runner.execute_scenario("command-current-pos")

    def test_remote_chrome_in_parallel(self):
        # Before running this test, make sure Selenium Grid has been set up locally
        # MAKE SURE TO VISUALLY CONFIRM (without headless) THIS TEST. Errors from multi-threaded processes
        # are not captured by the unittest framework
        threads = []
        number_of_sessions = range(3)
        for session in number_of_sessions:
            t = threading.Thread(target=self.test_remote_chrome)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


if __name__ == '__main__':
    unittest.main()
