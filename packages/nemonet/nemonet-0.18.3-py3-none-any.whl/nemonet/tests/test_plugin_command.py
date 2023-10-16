# Created by Jan Rummens at 12/01/2021
import unittest
import copy
from nemonet.runner.runner import Runner
from nemonet.engines.cache_store import KeyValueStore

import logging.config

logging.config.fileConfig(fname='../../vision_logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class CommandsTestCase(unittest.TestCase):

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

        self.runner = Runner(config=self.config)
        kv_store = KeyValueStore()
        kv_store.add("VISION_ENV_SCREENSHOTS","false")
        kv_store.close()

    def tearDown(self) -> None:
        # quit driver of runner that weren't used (didn't call execute_scenario)
        if not self.runner.driver.has_quit():
            self.runner.driver.quit()

    def test_plugins(self):
        self.runner.execute_scenario("commands-plugins")
        with open('ReadAndStore.txt', encoding="utf-8") as f:
            read_data = f.read()
            self.assertTrue(read_data == 'nemonet.tests.units.plugin.vision_my_custom_1')
            f.close()


if __name__ == '__main__':
    unittest.main()
