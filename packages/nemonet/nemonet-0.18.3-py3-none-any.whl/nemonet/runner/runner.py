# Created by Jan Rummens at 3/12/2020
import logging

from nemonet.screencast.web_screen import ImageRecording

logger = logging.getLogger(__name__)

from nemonet.engines.graph import Graph
from nemonet.engines.sequencer import Sequences
from nemonet.seleniumwebdriver.commands import Command
from nemonet.runner.tool import SeleniumTool
import json
import time


class RunnerError(Exception):
    pass


class Runner(object):

    @classmethod
    @property
    def default_config(cls):
        return {
            "driver": {
                "tool": "selenium",
                "tool_config": SeleniumTool.default_config
            },
            "screen_recording": {
                "enable": False
            }
        }

    def __init__(self, config=None):

        self.config = config
        self.driver = None
        self.has_passed = False
        self.stream = ImageRecording()

        if not self.config:
            self.config = self.default_config

        self._set_up_driver()

    def _set_up_driver(self):
        tool = self.config["driver"]["tool"]
        tool_config = self.config["driver"]["tool_config"]

        if tool == "selenium":
            self.driver = SeleniumTool.setup_driver(tool_config)
            self.driver.open()
        else:
            raise(RunnerError(f"{tool} is not a supported testing tool"))

    def turn_on_recording(self):
        if not self.is_recording:
            self.screenrecording.start()
            self.is_recording = True
            time.sleep(0.25)

    def turn_off_recording(self):
        if self.is_recording:
            self.screenrecording.stop()
            time.sleep(0.25)

    def scenario_passed(self):
        return self.has_passed

    def get_image_recorder(self):
        return self.stream

    def execute_scenario(self, xml_files_name):
        graph = Graph()
        graph.build(xml_files_name)
        sequences = Sequences(graph)
        commands = Command(self.driver.get_native_driver())
        commands.set_image_recorder(self.stream)
        commands.executeSequences(sequences, graph)
        self.driver.quit()
        self.has_passed = True

    @classmethod
    def from_json_file(cls, runner_config_filepath):
        with open(runner_config_filepath, 'r') as fp:
            return cls(config=json.load(fp))
