import random
import string

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from nemonet.cvision.computer_vision import ComputerVision
from nemonet.engines.cache_store import KeyValueStore
from nemonet.engines.graph import Action
from nemonet.seleniumwebdriver.abstract_command import AbstractCommand
from nemonet.seleniumwebdriver.page_capture import PageCapturing


class ClickableCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        xpath_str = action.getXpathStr()
        wait = WebDriverWait(driver, 60)
        element = wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        actions.click()
        actions.perform()


class ClickableDoubleCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        xpath_str = action.getXpathStr()
        wait = WebDriverWait(driver, 60)
        element = wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        actions.double_click(element)
        actions.perform()


class TextableCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        rStr = action.getValue()
        if (rStr == None):
            rStr = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        wait = WebDriverWait(driver, 60)
        element = wait.until(ec.visibility_of_element_located((By.XPATH, action.getXpathStr())))
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        actions.click()
        actions.send_keys(rStr)
        actions.perform()


class JSexecCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        driver.execute_script(action.getXpathStr())


class SelectableCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        wait = WebDriverWait(driver, 60)
        element = wait.until(ec.visibility_of_all_elements_located((By.XPATH, action.getXpathStr())))
        actions = ActionChains(driver)
        actions.move_to_element(element[2]).perform()
        actions.click()
        actions.perform()


class OpenURLCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        driver.get(str(action.getValue()))


class ScreenshotCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        filename = action.getValue()
        capture = PageCapturing(driver)
        capture.capture_save(file_name_cpatured=filename)


class ClearTextableCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        rStr = action.getValue()
        if rStr == None:
            rStr = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        wait = WebDriverWait(driver, 60)
        element = wait.until(ec.visibility_of_element_located((By.XPATH, action.getXpathStr())))
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("arguments[0].value = '';", "")
        self.sleep(0.25)
        actions = ActionChains(driver)
        element.clear()
        actions.move_to_element(element).perform()
        element.clear()
        actions.click()
        actions.send_keys(rStr)
        actions.perform()


class ClearTextableTabCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        rStr = action.getValue()
        if rStr == None:
            rStr = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        wait = WebDriverWait(driver, 60)
        element = wait.until(ec.visibility_of_element_located((By.XPATH, action.getXpathStr())))
        actions = ActionChains(driver)
        element.clear()
        actions.move_to_element(element).perform()
        actions.click()
        actions.send_keys(rStr)
        actions.send_keys(Keys.TAB)
        actions.perform()


class TextableEnterCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        rStr = action.getValue()
        if rStr == None:
            rStr = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        wait = WebDriverWait(driver, 60)
        element = wait.until(ec.visibility_of_element_located((By.XPATH, action.getXpathStr())))
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.click()
        actions.send_keys(rStr)
        actions.send_keys(Keys.RETURN)
        actions.perform()


class ComparePNGCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        arguments = eval(action.getValue())
        filenameA = arguments[0]
        filenameB = arguments[1]
        cv = ComputerVision()
        result = cv.diff(filenameA, filenameB)
        assert result, 'Difference between %s and %s' % (filenameA, filenameB)


class ComparePNGHashCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        arguments = eval(action.getValue())
        filenameA = arguments[0]
        filenameB = arguments[1]
        cv = ComputerVision()
        result = cv.diff_with_phash_image_hash(filenameA, filenameB)
        assert result, 'Difference between %s and %s' % (filenameA, filenameB)


class WaitCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        self.sleep(int(action.getValue()))


class ScrollTopCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        driver.execute_script("window.scrollTo(0,0);")


class ScrollBottomCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


class BrowserTabsGoToCurrentCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        driver.switch_to.window(driver.current_window_handle)


class TextCurrentPositionCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        actions = ActionChains(driver)
        actions.send_keys(action.getValue())
        actions.perform()


class TextCurrentPositionStampCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        text = action.getValue()
        actions = ActionChains(driver)
        text = text + " " + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        actions.send_keys(text)
        actions.perform()


class TabCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB)
        actions.perform()


class ClickableRightCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        wait = WebDriverWait(driver, 60)
        element = wait.until(ec.visibility_of_element_located((By.XPATH, action.getXpathStr())))
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        actions.context_click(element)
        actions.perform()


class DragAndDropCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        wait = WebDriverWait(driver, 60)
        xpath_from = action.getXpathStr()
        xpath_to = action.getValue()
        element_from = wait.until(ec.visibility_of_element_located((By.XPATH, xpath_from)))
        element_to = wait.until(ec.visibility_of_element_located((By.XPATH, xpath_to)))
        actions = ActionChains(driver)
        actions.move_to_element(element_from).perform()
        actions.drag_and_drop(element_from, element_to)
        actions.perform()


class DragAndDropMouseCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        wait = WebDriverWait(driver, 60)
        xpath_from = action.getXpathStr()
        to_xpath = action.getValue()
        element_from = wait.until(ec.visibility_of_element_located((By.XPATH, xpath_from)))
        element_to = wait.until(ec.visibility_of_element_located((By.XPATH, to_xpath)))
        actions = ActionChains(driver)
        actions.click(element_from)
        actions.perform()
        self.sleep(0.25)
        actions.click_and_hold(element_from)
        actions.move_to_element(element_to)
        actions.perform()
        self.sleep(0.25)
        actions.release()
        self.sleep(0.25)
        actions.perform()


class GoToFrameCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        frame_nbr = action.getValue()
        driver.switch_to.frame(int(frame_nbr))


class DragAndDropWithOffsetCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        wait = WebDriverWait(driver, 60)
        xpath_from = action.getXpathStr()
        offsets = action.getValue()
        offsets = offsets.split(',')
        element_from = wait.until(ec.visibility_of_element_located((By.XPATH, xpath_from)))
        actions = ActionChains(driver)
        actions.move_to_element(element_from).perform()
        self.sleep(0.25)
        actions.drag_and_drop_by_offset(element_from, offsets[0], offsets[1])
        self.sleep(0.25)
        actions.perform()


class SwitchToAlertAndConfirmCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        the_alert = driver.switch_to.alert
        the_alert.accept()


class RemoveHTMLElementCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        wait = WebDriverWait(driver, 60)
        css_selector = action.getValue()
        element_css_selector = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        self.sleep(0.25)
        driver.execute_script("arguments[0].scrollIntoView();", element_css_selector)
        self.sleep(0.25)
        driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element_css_selector)


class SaveCurrentURLCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        kv_store = KeyValueStore()
        kv_store.add(action.get_key(), driver.current_url)
        kv_store.close()


class SplitStoredURLCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        url_key = action.get_key()
        kv_store = KeyValueStore()
        url = kv_store.get_value_as_str(url_key)
        split_url = url.split('//')[1].split('/')
        counter = 1
        for section in split_url:
            if len(section) > 0:
                url_key_nbr = url_key + "_" + str(counter)
                counter += 1
                kv_store.add(url_key_nbr, section)
        kv_store.close()


class FormatStringsCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        value = action.getValue()
        key = action.get_key()
        kv_store = KeyValueStore()
        reformated_str = kv_store.replace_formated_key(value)
        kv_store.add(key, reformated_str)
        kv_store.close()


class StoreStringCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        value = action.getValue()
        key = action.get_key()
        kv_store = KeyValueStore()
        kv_store.add(key, value)
        kv_store.close()


class SplitURLAndStoreCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        value = action.getValue()
        key_prefix = action.get_key()
        split_url = value.split('//')[1].split('/')
        kv_store = KeyValueStore()
        counter = 1
        for section in split_url:
            if len(section) > 0:
                url_key_nbr = key_prefix + "_" + str(counter)
                counter += 1
                kv_store.add(url_key_nbr, section)
        kv_store.close()


class SelectFromDropDownCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        wait = WebDriverWait(driver, 60)
        locator = (By.XPATH, action.getXpathStr())
        element = wait.until(ec.element_to_be_clickable(locator), message='Cannot locate {}'.format(locator))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        Select(element).select_by_visible_text(action.getValue())


class SiteSettingsCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        site_setting_url_and_tab_nbr_list = action.getValue().split('|')
        url = site_setting_url_and_tab_nbr_list[0]
        tab_nbr = site_setting_url_and_tab_nbr_list[1]
        set_back_url = driver.current_url
        driver.get(str(url))  # open url
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB * int(tab_nbr))
        actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()
        self.sleep(0.25)
        driver.get(str(set_back_url))  # open url


class TabsAndEnterCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        tab_nbr = action.getValue()
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB * int(tab_nbr))
        actions.send_keys(Keys.RETURN)
        actions.perform()
        self.sleep(0.25)


class TabsAndTextCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        values = action.getValue().split(':')
        tab_nbr = values[0]
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB * int(tab_nbr))
        actions.send_keys(values[1])
        actions.perform()
        self.sleep(0.25)


class BrowserTabsAddCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        nbr_of_tabs = int(action.getValue())
        self.log(driver.current_window_handle)
        for nbr in range(nbr_of_tabs):
            tab_name = "TAB_" + str(nbr)
            driver.execute_script("window.open('about:blank', '%s');" % (tab_name))
            self.sleep(0.5)
            driver.switch_to.window(tab_name)
            self.log(driver.current_window_handle)


class BrowserTabsGoToCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        tab_nbr = int(action.getValue())
        handles = driver.window_handles
        self.log(handles)
        driver.switch_to.window(handles[tab_nbr])


class LogCurrentURLCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        self.log(driver.current_url)


class OpenStoredURLCommand(AbstractCommand):
    def execute_action(self, action: Action, driver):
        kv_store = KeyValueStore()
        stored_key = action.get_key()
        url = kv_store.get_value_as_str(stored_key)
        self.log(url)
        driver.get(str(url))  # open url


class SetEnvironmentVariable(AbstractCommand):
    def execute_action(self, action: Action, driver):
        value = action.getValue()
        key_to_store = action.get_key()
        value_to_store = action.getValue()
        kv_store = KeyValueStore()
        kv_store.add(key_to_store, value_to_store)
        kv_store.close()


class SelectorExists(AbstractCommand):
    """
        Check if the specified selector is available in the screen
        On failure let it throw an exception
    """

    def execute_action(self, action: Action, driver):
        xpath_str = action.getXpathStr()
        wait = WebDriverWait(driver, 60)
        wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))


class GetValueAndCompare(AbstractCommand):
    """
        Get the value from the selector
        On failure let it throw an exception
    """

    def execute_action(self, action: Action, driver):
        xpath_str = action.getXpathStr()
        value = str(action.getValue())
        wait = WebDriverWait(driver, 60)
        element = wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        assert value == str(element.text)


class GetTextAndStore(AbstractCommand):
    """
        Get the value from the selector and store the value
        On failure let it throw an exception
    """

    def execute_action(self, action: Action, driver):
        xpath_str = action.getXpathStr()
        key = str(action.get_key())
        wait = WebDriverWait(driver, 60)
        element = wait.until(ec.visibility_of_element_located((By.XPATH, xpath_str)))
        kv_store = KeyValueStore()
        kv_store.add(key, str(element.text))
        kv_store.close()
