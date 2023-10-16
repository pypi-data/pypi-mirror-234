from abc import ABC, abstractmethod
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestDriver(ABC):

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def quit(self):
        pass

    @abstractmethod
    def has_quit(self) -> bool:
        pass


class ChromeTestDriver(TestDriver):

    @classmethod
    @property
    def default_config(cls) -> dict:
        return {
            "headless": False,
            "experimental_flags": None,
            "remote_settings": None
        }

    def __init__(self, config=None):

        if not config:
            config = self.default_config

        self._experimental_flags = None
        self._experimental_flags = False
        self._remote_settings = None
        self._driver = None
        self._session_id = None

        if "remote_settings" in config.keys():
            self._remote_settings = config["remote_settings"]
        if "experimental_flags" in config.keys():
            self._experimental_flags = config["experimental_flags"]
        if "headless" in config.keys():
            self._headless = config["headless"]

    @property
    def experimental_flags(self) -> list:
        ef = self._experimental_flags
        if ef:
            return deepcopy(ef)
        else:
            return []

    @property
    def headless(self) -> bool:
        return self._headless

    @property
    def remote_settings(self) -> dict:
        rs = self._remote_settings
        if rs:
            return deepcopy(rs)
        else:
            return {}

    @property
    def options(self) -> Options:
        """ returns an instance of ChromeOptions based on current configuration """
        options = Options()
        if self.experimental_flags:
            chrome_local_state_prefs = {'browser.enabled_labs_experiments': self.experimental_flags}
            options.add_experimental_option('localState', chrome_local_state_prefs)
        if self.headless:
            options.add_argument("--headless")
        return options

    def open(self):
        if self.remote_settings:
            kwargs = self.remote_settings
            kwargs["options"] = self.options
            self._driver = webdriver.Remote(**kwargs)
        else:
            self._driver = webdriver.Chrome(options=self.options)
        self._session_id = self._driver.session_id
        self._driver.maximize_window()

    def quit(self):
        self._driver.quit()
        self._session_id = None

    def has_quit(self):
        if self._session_id:
            return False
        return True

    def get_native_driver(self) -> webdriver.Chrome:
        return self._driver
