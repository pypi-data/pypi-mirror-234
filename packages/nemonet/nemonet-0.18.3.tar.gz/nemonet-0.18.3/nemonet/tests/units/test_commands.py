""" Unittest for the abstract_command.py module """

# python packages
import unittest

# vision packages
from nemonet.engines.graph import Action
from nemonet.seleniumwebdriver.commands import Command


class TestCommands(unittest.TestCase):

    def setUp(self):
        self.dummy_graph_action = Action("some_xpathstring", "DUMMY", value="value", wait_after=3, key="something")
        self.dummy_driver = "TEST_DRIVER"
        self.dummy_command = Command(self.dummy_driver)

    def tearDown(self):
        pass

    def test_dummy_command(self):
        dummy_command_class = self.dummy_command.execute_command(self.dummy_graph_action)
        self.assertIsNone(dummy_command_class, msg="dummy command class should be None")

    def test_unknown_command(self):
        unknown_graph_action = Action("this type should not exist", "@m$acL9QiXaSKdRe")
        with self.assertRaises(AssertionError, msg="Unknown commands should throw an error"):
            self.dummy_command.execute_command(unknown_graph_action)


if __name__ == '__main__':
    unittest.main()
