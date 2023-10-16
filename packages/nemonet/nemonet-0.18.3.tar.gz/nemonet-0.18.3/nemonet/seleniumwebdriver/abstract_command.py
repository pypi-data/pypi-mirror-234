import logging
logger = logging.getLogger(__name__)

import time
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

from nemonet.engines.graph import Action
from nemonet.seleniumwebdriver.page_capture import PageCapturing
from nemonet.engines.cache_store import KeyValueStore

class AbstractCommand(ABC):

    @abstractmethod
    def execute_action(self, action: Action, driver):
        pass  # does nothing by default

    def set_image_recorder(self, image_recorder):
        self.image_recorder = image_recorder

    def execute(self, action: Action, driver, sleep_time=0.25, filename=None):
        """ Executes given action as a vision command """

        self.__sleep(sleep_time)
        self.__screenshot(action, driver)
        self.__log(str(action))
        self.execute_action(action, driver)
        self.__sleep(sleep_time)
        self.__screenshot(action, driver)
        self.__sleep(action.get_wait_after())

    def log(self, string):
        self.__log(string)

    def sleep(self, second):
        self.__sleep(second)

    def __screenshot(self, action, driver):
        """ Takes a screenshot of the current state of [ TERMINOLOGY ] using given driver
            and saves it as a .png file with given filename [ WHERE? ].
            Fails silently when given filename is None. """
        if action == None:
            return
        if action.getElementType() == 'SCREENSHOT':
            return
        if not self.image_recorder.is_enabled():
            return
        capture = PageCapturing(driver)
        capture.capture_save(file_name_cpatured=self.image_recorder.generate_screenshot_filename(action.getElementType()))

    def __sleep(self, seconds):
        time.sleep(seconds)

    def __log(self, string):
        # TODO : recomputation should be avoided
        # set up
        # log
        logger.debug(string)
