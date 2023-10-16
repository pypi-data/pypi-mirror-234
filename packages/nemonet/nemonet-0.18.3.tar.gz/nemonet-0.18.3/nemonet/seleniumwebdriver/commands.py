'''
Created on 13 feb. 2018

@author: ex03210
'''
import configparser
import inspect
import logging
import sys
from importlib import import_module
from os import walk

from nemonet.screencast.web_screen import ImageRecording

logger = logging.getLogger(__name__)

from nemonet.seleniumwebdriver.command_list import *


class Command(object):
    """
        All kind of selenium actions and more
    """

    def __init__(self, driver=None):
        """Constructor"""
        self.driver = driver
        self._wait = WebDriverWait(self.driver, 60)
        self.image_recorder = None
        # on construction, we need to provide the plugin commands
        try:
            self.build_plugins()
        except Exception as e:
            logger.info("No plugins added " + str(e))

    def set_image_recorder(self, image_recorder):
        self.image_recorder = image_recorder

    def has_cache_screenshots_enabled(self):
        try:
            kv_store = KeyValueStore()
            value_true_false = kv_store.get_value_as_str("VISION_ENV_SCREENSHOTS")
            kv_store.close()

            if value_true_false.lower() == 'false':
                return False
            else:
                return True
        except:
            logger.debug("Error KeyValue Store ", exc_info=True)
        return False

    def executeSequences(self, seq, g):
        # this is the entrypoint for enabling the recording
        # the idea is to set the recording globally per scenario in the setup phase.
        # disable certain actions from being performed other than the setup e.g. VISION_ENV_SCREENSHOTS = True

        for step in g.getSetup():
            logger.debug("Action: " + str(step.getAction()))
            self.execute_command(step.getAction())
        # environment variable that enables the screenrecording is persisted in the cache.hdf5
        # @TODO : check if image recorder is on
        if self.has_cache_screenshots_enabled():
            logger.debug("VISION_ENV_SCREENSHOTS is true")
            self.image_recorder.enable_recording()
        #
        pa = seq.get()
        for l in pa:
            # logger.info("Execute sequence=%s" % (str(l)))
            for el in l:
                a = g.getVertex(el).getAction()
                self.execute_command(a)

    def execute_command(self, action: Action):
        """
        TODO : error handling
        :param action:
        :return:
        """
        command_type = action.getElementType()

        try:
            command_class = commands[command_type]
            if (command_class == None):
                pass  # Dummy Command for testing purposes
            else:
                c = command_class()
                c.set_image_recorder(self.image_recorder)
                c.execute(action, self.driver)
                return c

        except KeyError:
            # TODO : AssertionError is too generic, in need of an UnknownCommandException
            logger.debug("Fatal Error KeyError ", exc_info=True)
            assert False, f"{command_type} is not a known command"

    def build_plugins(self):
        # use a configuration file approach
        config = configparser.ConfigParser()
        # is expected to have the cfg in the current folder
        config.read('vision.cfg')  # failure wrong name => KeyError
        logger.debug("Config file is read")
        # review this way of resolving the path to the plugin directory
        logger.debug(config.sections())
        # config file needed to specify the path to the plugin folder
        mypath = config['PLUGIN']['PluginDir']
        logger.debug("Plugin Folder= %s" % (mypath))
        vision_modules = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            vision_modules.extend(filenames)
        filtered = list(filter(lambda vision_module: vision_module.startswith("vision_"), vision_modules))
        # remove compiled occurrences .pyc
        filtered = [item for item in filtered if '.pyc' not in item]
        filtered = [w.removesuffix('.py') for w in filtered]
        # look for a plugin directory and determine the plugin package directory
        # example below retrieves instance of the module
        # maybe best is to add to config file
        classes_as_spec = []  # result classes after checking the class protocol
        for mod in filtered:
            logger.debug("Import module= %s" % (config['PLUGIN']['PackageName']))
            m2 = import_module('.' + mod, package=config['PLUGIN']['PackageName'])
            logger.debug("Import module instance= %s" % (m2))
            # get the classes from the module
            classes = [cls_name for cls_name, cls_obj in inspect.getmembers(sys.modules[m2.__name__]) if
                       inspect.isclass(cls_obj)]
            logger.debug("classes from the module= %s" % (classes))
            # inspect what class has the correct method signature
            for cls in classes:
                is_vision_class = getattr(m2, cls)
                if hasattr(is_vision_class,
                           "execute_action") and is_vision_class.__base__.__name__ == 'AbstractCommand':
                    classes_as_spec.append(is_vision_class)
                    #below gives failure
                    logger.info("Added plugin " + is_vision_class().command_name())
                    #commands[is_vision_class(self).command_name()] = is_vision_class
                    commands[is_vision_class().command_name()] = is_vision_class

# TODO : this variable is exposed and needs a better location
commands = {
    'DUMMY': None,
    'CLICKABLE': ClickableCommand,
    'CLICKABLE_DOUBLE': ClickableDoubleCommand,
    'TEXTABLE': TextableCommand,
    'JSexec': JSexecCommand,
    'SELECTABLE': SelectableCommand,
    'OPENURL': OpenURLCommand,
    'SCREENSHOT': ScreenshotCommand,
    'CLEARTEXTABLE': ClearTextableCommand,
    'CLEARTEXTABLETAB': ClearTextableTabCommand,
    'TEXTABLE-ENTER': TextableEnterCommand,
    'COMPAREPNG': ComparePNGCommand,
    'COMPAREPNGPHASH': ComparePNGHashCommand,
    'WAIT': WaitCommand,
    'SCROLLTOP': ScrollTopCommand,
    'SCROLLBOTTOM': ScrollBottomCommand,
    'TAB': TabCommand,
    'CLICKABLE_RIGHT': ClickableRightCommand,
    'DRAG_AND_DROP': DragAndDropCommand,
    'GOTO_FRAME': GoToFrameCommand,
    'SAVE_CURRENT_URL': SaveCurrentURLCommand,
    'SPLIT_STORED_URL': SplitStoredURLCommand,
    'FORMAT_STRINGS': FormatStringsCommand,
    'STORE_STRING': StoreStringCommand,
    'SITE_SETTINGS': SiteSettingsCommand,
    'TABS_AND_ENTER': TabsAndEnterCommand,
    'TABS_AND_TEXT': TabsAndTextCommand,
    'BROWSER_TABS_ADD': BrowserTabsAddCommand,
    'BROWSER_TABS_GOTO': BrowserTabsGoToCommand,
    'LOG_CURRENT_URL': LogCurrentURLCommand,
    'OPEN_STORED_URL': OpenStoredURLCommand,
    'BROWSER_TABS_GOTO_CURRENT': BrowserTabsGoToCurrentCommand,
    'TEXT_CURRENT_POSITION': TextCurrentPositionCommand,
    'TEXT_CURRENT_POSITION_STAMP': TextCurrentPositionStampCommand,
    'DRAG_AND_DROP_MOUSE': DragAndDropMouseCommand,
    'DRAG_AND_DROP_WITH_OFFSET': DragAndDropWithOffsetCommand,
    'SWITCH_TO_ALERT_AND_CONFIRM': SwitchToAlertAndConfirmCommand,
    'REMOVE_HTML_ELEMENT': RemoveHTMLElementCommand,
    'SPLIT_URL_AND_STORE': SplitURLAndStoreCommand,
    'SELECT_FROM_DROP_DOWN': SelectFromDropDownCommand,
    'SET_VISION_ENV': SetEnvironmentVariable,
    'SEL_EXISTS': SelectorExists,
    'GET_VALUE_AND_COMPARE': GetValueAndCompare,
    'GET_TEXT_AND_STORE': GetTextAndStore
}
