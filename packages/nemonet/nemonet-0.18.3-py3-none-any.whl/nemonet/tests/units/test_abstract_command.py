""" Unittest for the abstract_command.py module """

# python packages
import unittest
import time

# vision packages
from nemonet.engines.graph import Action
from nemonet.seleniumwebdriver.abstract_command import AbstractCommand


""" - - - classes to be used only for testing purposes - - - """

class _DummySubclass(AbstractCommand):

    """ a valid subclass of AbstractCommand """

    def execute_action(self, action: Action, driver):
         return action.getElementType() + " " + driver


""" - - - unittests - - - """

class TestAbstractCommand(unittest.TestCase):

    def setUp(self):

        self.dummy_graph_action = Action("some_xpathstring", "TEST_TYPE", value="value", wait_after= 3, key = "something")
        self.dummy_driver = "TEST_DRIVER"

    def tearDown(self):

        pass

    def test_abstract_command_should_not_instantiate(self):

        with self.assertRaises(TypeError, msg="Abstract Class should not instantiate"):
            AbstractCommand()

    def test_subclasses_should_instantiate(self):

        _DummySubclass()

    def test_execute_command_sleep(self):

        sleep = 5
        before = time.time()
        _DummySubclass().execute(self.dummy_graph_action, self.dummy_driver, sleep_time=sleep)
        after = time.time()

        self.assertTrue(after - before > ((sleep * 2) - 1), "Vision command did not sleep long enough")

    def test_execute_command_screenshot(self):

        # TODO
        # _DummySubclass().execute(self.dummy_graph_action, self.dummy_driver, filename="Hello, World")
        pass

    def test_execute_action(self):

        actual      = _DummySubclass().execute_action(self.dummy_graph_action, self.dummy_driver)
        expected    = self.dummy_graph_action.getElementType() + " " + self.dummy_driver

        self.assertEqual(expected, actual)

    def test_log(self):

        def extract_words_from_line(string : str, words : int):
            temp = string.split(" ")
            return ' '.join(temp[-words:]).replace('\n','')

        # what I want to log
        expect = "Hello, world!"

        # what is actually logged
        _DummySubclass().log(expect)
        with open('vision.log', 'r') as log:
            for line in log:
                pass
            last_line = line
        actual = extract_words_from_line(last_line, 2)

        self.assertEqual(expect, actual, msg=f"logging not working as expected")


if __name__ == '__main__':
    unittest.main()


