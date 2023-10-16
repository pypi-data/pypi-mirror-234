from nemonet.seleniumwebdriver.abstract_command import AbstractCommand
from nemonet.engines.graph import Action


class ScreenDump(AbstractCommand):
    def execute_action(self, action: Action, driver):
        pass

    def command_name(self) -> str:
        return 'SCREEN_DUMP'


class FancyCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        pass

    def command_name(self) -> str:
        return 'FANCY_COMMAND'
