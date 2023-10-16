import os
import unittest
import time
import pyscreeze
from nemonet.screencast.web_screen import ImageRecording
import re

class MyTestCase(unittest.TestCase):

    def test_something(self):
        image_recorder = ImageRecording()
        image_recorder.enable_recording()
        screenshot_filename = image_recorder.generate_screenshot_filename("OPENURL")
        filename_without_path = os.path.basename(screenshot_filename)
        print(filename_without_path)
        self.assertTrue( filename_without_path.startswith('screenshot_') )
        m = re.search('screenshot_([0-9]{8})-([0-9]{6})\.([0-9]{6})-([A-Z]+)-([a-z|0-9]{8})-([a-z|0-9]{4})-([a-z|0-9]{4})-([a-z|0-9]{4})-([a-z|0-9]{12})\.(png)', filename_without_path)
        self.assertTrue(len(m.groups()) == 10)
        self.assertTrue(m.groups()[9] == 'png')
        self.assertTrue(m.groups()[3] == 'OPENURL')

    def test_avi_zip(self):
        image_recorder = ImageRecording()
        image_recorder.enable_recording()
        for nbr in range(0,10):
            pyscreeze.screenshot(image_recorder.generate_screenshot_filename(str(nbr)))
            time.sleep(0.25)
        image_recorder.store()

if __name__ == '__main__':
    unittest.main()
