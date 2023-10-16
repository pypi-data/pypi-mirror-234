# Created by Jan Rummens at 5/01/2021
import os
import unittest
import json
from nemonet.runner.runner import Runner, RunnerError


class RunnerConfigTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.filename = 'runner_config.json'
        self.default_config_dict = Runner.default_config

        with open( self.filename, 'w') as fp:
            json.dump(self.default_config_dict, fp, indent=4)

    def tearDown(self) -> None:
        os.remove(self.filename)

    def test_runner_init_from_file(self):
        """ There should be no difference between instantiating a Runner "normally" and
            from a json file """

        r1 = Runner(self.default_config_dict)
        r2 = Runner.from_json_file(self.filename)

        for data in [r1.config, r2.config]:
            self.assertTrue( list( data.keys() ) == ['driver', 'screen_recording'] )
            self.assertTrue( list( data["driver"].keys() ) == ['tool', 'tool_config'] )
            self.assertTrue( list( data["screen_recording"].keys()) == ['enable'] )

    def test_runner_raises_error(self):

        config = self.default_config_dict
        config["driver"]["tool"] = "unsupported tool"

        with self.assertRaises(RunnerError):
            Runner(config=config)


if __name__ == '__main__':
    unittest.main()
