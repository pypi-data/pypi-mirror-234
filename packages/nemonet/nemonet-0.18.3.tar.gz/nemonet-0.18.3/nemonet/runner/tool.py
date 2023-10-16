from nemonet.runner.webdriver import TestDriver, ChromeTestDriver

class WebdriverError(Exception):
    pass

class SeleniumTool:

    @classmethod
    @property
    def default_config(cls) -> dict:
        return {
            "webdriver": "chrome",
            "webdriver_config": ChromeTestDriver.default_config
        }

    @classmethod
    def setup_driver(cls, config=None) -> TestDriver:

        """ returns an instance of a TestDriver based on given selenium config """

        if not config:
            config = cls.default_config

        webdriver = config["webdriver"]

        if webdriver == "chrome":
            return ChromeTestDriver(config["webdriver_config"])
        else:
            raise(WebdriverError(f"{webdriver} is not a supported webdriver"))