from nemonet.seleniumwebdriver.abstract_command import AbstractCommand
from nemonet.engines.graph import Action
import inspect

class ReadAndStore(AbstractCommand):
    def execute_action(self, action: Action, driver):
        m = inspect.getmodule(self)
        with open('ReadAndStore.txt', 'w') as f:
            f.write(m.__name__)
            f.close()

    def command_name(self) -> str:
        return 'READ_AND_STORE'
