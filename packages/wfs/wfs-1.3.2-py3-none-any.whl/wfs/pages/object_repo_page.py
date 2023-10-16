from wfs.utils.action_test_item import *
from poium import Page
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from cdxg.appium_lab import AppiumLab
from waiting import wait
import time
from pathlib import Path
import traceback
mypath = Path.cwd()


def get_find_element(driver: WebDriver, element, locate, action_item, text=None):
    locatorx = (locate, element)
    if text is not None:
        if action_item == 'text' or action_item == 'link_text':
            getalltext = WebDriverWait(driver, 30).until(ec.text_to_be_present_in_element(locatorx, text))
            gtext = None
            if getalltext:
                gtext = text
            return gtext
    else:
        return WebDriverWait(driver, 30).until(ec.visibility_of_element_located(locator=locatorx))


def get_find_elements(driver: WebDriver, element, locate, action_item, text=None):
    locatorx = (locate, element)
    if text is not None:
        if action_item == 'text':
            getalltext = WebDriverWait(driver, 30).until(ec.text_to_be_present_in_element(locatorx, text))
            gtext = None
            if getalltext:
                gtext = text
            return gtext
    else:
        return WebDriverWait(driver, 30).until(ec.visibility_of_all_elements_located(locator=locatorx))


class Object_Repo_Page(Page):

    def __int__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def locators_ready(self, greadyx, textn=None):
        elementlocate, action_item = None, None
        locator_identity, element_identity, action_item, fetchlements = greadyx
        if locator_identity == 'id_' and fetchlements == 'S' or locator_identity == 'id' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, element_identity, By.ID, action_item, text=textn)
        elif locator_identity == 'id_' and fetchlements == 'M' or locator_identity == 'id' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, element_identity, By.ID, action_item, text=textn)
        elif locator_identity == 'xpath' and fetchlements == 'S' or locator_identity == 'XPATH' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, element_identity, By.XPATH, action_item, text=textn)
        elif locator_identity == 'xpath' and fetchlements == 'M' or locator_identity == 'XPATH' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, element_identity, By.XPATH, action_item, text=textn)
        elif locator_identity == 'apacid' and fetchlements == 'S' or locator_identity == 'APACID' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, element_identity, AppiumBy.ACCESSIBILITY_ID, action_item)
        elif locator_identity == 'apacid' and fetchlements == 'M' or locator_identity == 'APACID' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, element_identity, AppiumBy.ACCESSIBILITY_ID, action_item)
        elif locator_identity == 'css' and fetchlements == 'S' or locator_identity == 'CSS' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, element_identity, By.CSS_SELECTOR, action_item, text=textn)
        elif locator_identity == 'css' and fetchlements == 'M' or locator_identity == 'CSS' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, element_identity, By.CSS_SELECTOR, action_item, text=textn)
        elif locator_identity == 'tag' and fetchlements == 'S' or locator_identity == 'TAG' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, element_identity, By.TAG_NAME, action_item, text=textn)
        elif locator_identity == 'tag' and fetchlements == 'M' or locator_identity == 'TAG' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, element_identity, By.TAG_NAME, action_item, text=textn)
        else:
            if locator_identity == 'class' and fetchlements == 'S' or locator_identity == 'CLASS' and fetchlements == 'S':
                elementlocate = get_find_element(self.driver, element_identity, By.CLASS_NAME, action_item, text=textn)
            elif locator_identity == 'class' and fetchlements == 'M' or locator_identity == 'CLASS' and fetchlements == 'M':
                elementlocate = get_find_elements(self.driver, element_identity, By.CLASS_NAME, action_item, text=textn)
            if locator_identity == 'apclass' and fetchlements == 'S' or locator_identity == 'APCLASS' and fetchlements == 'S':
                elementlocate = get_find_element(self.driver, element_identity, AppiumBy.CLASS_NAME, action_item,
                                                 text=textn)
            elif locator_identity == 'apclass' and fetchlements == 'M' or locator_identity == 'APCLASS' and fetchlements == 'M':
                elementlocate = get_find_elements(self.driver, element_identity, AppiumBy.CLASS_NAME, action_item,
                                                  text=textn)
            elif locator_identity == 'apid' and fetchlements == 'S' or locator_identity == 'APID' and fetchlements == 'S':
                elementlocate = get_find_element(self.driver, element_identity, AppiumBy.ID, action_item, text=textn)
            elif locator_identity == 'apid' and fetchlements == 'M' or locator_identity == 'APID' and fetchlements == 'M':
                elementlocate = get_find_elements(self.driver, element_identity, AppiumBy.ID, action_item, text=textn)
            elif locator_identity == 'apxpath' and fetchlements == 'S' or locator_identity == 'apXPATH' and fetchlements == 'S':
                elementlocate = get_find_element(self.driver, element_identity, AppiumBy.XPATH, action_item, text=textn)
            elif locator_identity == 'apxpath' and fetchlements == 'M' or locator_identity == 'APXPATH' and fetchlements == 'M':
                elementlocate = get_find_element(self.driver, element_identity, AppiumBy.XPATH, action_item, text=textn)
            else:
                pass
        # print(elementlocate)
        return elementlocate

    def clickable_element(self, greadyx):
        locator_identity, element_identity, action_item, fetchlements = greadyx  # , gitem = getjsonlist()
        get_elements_to_find = find_element_click(by=locator_identity, expression=element_identity,
                                                  search_window=self.driver, felements=fetchlements)
        # print(len(get_elements_to_find))
        return get_elements_to_find  # find_element_click(by=locator_identity, expression=element_identity, search_window=self.driver)

    def element_in_frames(self, greadyx):
        locator_identity, element_identity, action_item, fetchlements = greadyx  # , gitems = getjsonlist()
        locatorsplit = locator_identity.split('**')
        # print(locatorsplit)
        frame_locator, dom_locator = locatorsplit
        elementsplit = element_identity.split('**')
        # print(elementsplit)
        frame_element, dom_element = elementsplit
        switch_in_frames(self.driver, frame_element, frame_locator, action_item)
        if dom_locator == 'id_' and fetchlements == 'S' or dom_locator == 'id' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, dom_element, By.ID, action_item)
        elif dom_locator == 'id_' and fetchlements == 'M' or dom_locator == 'id' and fetchlements == 'M':
            elementlocate = get_find_elements(self.driver, dom_element, By.ID, action_item)
        elif dom_locator == 'xpath' and fetchlements == 'S' or dom_locator == 'XPATH' and fetchlements == 'S':
            elementlocate = get_find_element(self.driver, dom_element, By.XPATH, action_item)
        else:
            elementlocate = get_find_elements(self.driver, dom_element, By.XPATH, action_item)
        return elementlocate

    def back_to_default(self):
        self.driver.switch_to.default_content()

    def gethidden(self, greadyx):
        locator_identity, element_identity, action_item, fetchlements = greadyx  # , gitems = getjsonlist()
        if locator_identity in ['css', 'js']:
            return self.driver.execute_script("return document.querySelector('" + str(element_identity) + "')")
        else:
            return 'No elements allowed other than CSS or JS'

    def get_inject_data(self, elements, attriname):
        elementx = []
        if len(elements) > 0:
            for i, element in enumerate(elements):
                random_value = attriname + '_' + str(i)  # f"aaa{i + 1}"
                self.driver.execute_script(f"arguments[0].setAttribute('id', '{random_value}');", element)
                return elementx.append(element)
        else:
            self.driver.execute_script(f"arguments[0].setAttribute('id', '{attriname}');", elements)
            return elementx.append(elements)

    def get_attribute_value(self, element, attribute_name):
        return self.driver.execute_script(f"return arguments[0].getAttribute('{attribute_name}');", element)

    def get_attribute_values(self, element):
        # Get all attributes and their values for the element
        element_attributes = self.driver.execute_script(
            "var items = {}; "  # Create an empty JavaScript object
            "for (var i = 0; i < arguments[0].attributes.length; i++) { "
            "  items[arguments[0].attributes[i].name] = arguments[0].attributes[i].value; "
            "} "
            "return items;", element)

        # Print the attributes and their values
        xattrib = []
        for attribute, value in element_attributes.items():
            xattrib.append(f"{attribute}: {value}")
        return xattrib

    def set_attributes_values(self, elements, attribValues):
        # Define the custom attribute name and values
        try:
            attribute_name = "id"
            attribute_values = attribValues  # Replace with your desired values
            # Iterate through the elements and set the custom attribute with distinct values
            xattrib = []
            # for i, element in enumerate(elements):
            for i in range(0, len(elements)):
                element = elements[i]
                attribute_value = attribute_values[i]
                self.driver.execute_script(f"arguments[0].setAttribute(arguments[1], arguments[2]);", element, attribute_name,
                                      attribute_value)
                xattrib.append(f"element {i + 1} to: {attribute_name}: {attribute_value}")
                # print(f"Set {attribute_name} for element {i + 1} to: {attribute_value}")
            return xattrib
        except Exception as e:
            print(str(e))
            traceback.print_exc()


    def get_inject_mobile_data(self, elements, attriname, ptname):
        element_attribute = elements
        element_value = attriname
        elementx = []
        if len(elements) > 0:
            if ptname == 'Android':
                for i, element in enumerate(elements):
                    random_value = attriname + '_' + str(i)  # f"aaa{i + 1}"
                    self.driver.execute_script('mobile: shell', {
                        'command': 'input',
                        'args': ['text', f'new UiSelector().description("{element_attribute}={element_value}")']
                    })
                    return elementx.append(element)
        else:
            self.driver.execute_script('mobile: shell', {
                'command': 'input',
                'args': ['text', f'[{element_attribute}="{element_value}"]']
            })
            return elementx.append(elements)
        # Android
        # element = driver.find_element(MobileBy.XPATH, f'//*[@content-desc="{element_attribute}={element_value}"]')
        # iOS
        # element = driver.find_element(MobileBy.XPATH, f'//*[@{element_attribute}="{element_value}"]')

    def getscrolled(self, elementx):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elementx)

    def get_action_chains(self):
        return ActionChains(self.driver)

    def go_to_previous_page(self, hide_keyboard: bool = False):
        if hide_keyboard:
            self.hide_keyboard()
        self.driver.back()

    def hide_keyboard(self):
        wait(lambda: self.driver.is_keyboard_shown(),
             timeout_seconds=10)
        self.driver.hide_keyboard()

    def get_current_url(self):
        return self.driver.current_url

    def get_touch_actions(self):
        return TouchAction(self.driver)

    def get_appium_lab(self):
        return AppiumLab(self.driver)

    def screen_shots(self, screenshot_path):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenName = f"failure_{screenshot_path}_{timestamp}.png"
        snamex = mypath / 'reports' / 'screenshots' / screenName
        self.driver.save_screenshot(str(snamex))
        return snamex


def object_repox(driver):
    return Object_Repo_Page(driver)


def find_element_click(by, expression, search_window=None, timeout=32, ignore_exception=None, poll_frequency=4,
                       felements=None):
    # print(felements)
    if ignore_exception is None:
        ignore_exception = []

    ignore_exception.append(NoSuchElementException)
    end_time = time.time() + timeout
    while True:
        try:
            by = elementRef(locatorIdentity=by)
            if felements == 'S':
                web_element = search_window.find_element(by=by, value=expression)
                search_window.execute_script("arguments[0].click();", web_element)
                return 'YY'
            else:
                web_element = search_window.find_elements(by=by, value=expression)
                return web_element
                # print(web_element)
                # web_element.click()
        except tuple(ignore_exception) as e:
            # print(str(e))
            if time.time() > end_time:
                # print(str(e))
                time.sleep(poll_frequency)
                break
        except Exception as e:
            raise
    return 'NN'


def getjsonlist(test_data_json):
    locator_identity, element_identity, action_item, fetchlements, gitem = None, None, None, None, None
    readxx = readlastine(test_data_json)
    if str(readxx) != 'NA':
        greadx = readxx.split('|')
        locator_identity = greadx[0]
        element_identity = greadx[1]
        action_item = greadx[5]
        fetchlements = greadx[7]
        gitem = greadx[8]
    return locator_identity, element_identity, action_item, fetchlements, gitem


def switch_in_frames(driver: WebDriver, element, locate, action_item):
    # print(element, locate, action_item)
    locatorx = (locate, element)
    return WebDriverWait(driver, 30).until(ec.frame_to_be_available_and_switch_to_it(locator=locatorx))


def wait_for_element_to_vanish(webelement):
    is_displayed = webelement.is_displayed()
    start_time = get_current_time_in_millis()
    time_interval_in_seconds = 5
    while is_displayed and not is_time_out(start_time, time_interval_in_seconds):
        is_displayed = webelement.is_displayed()
    return not is_displayed


def click_until_interactable(webelement):
    element_is_interactable = False
    start_time = get_current_time_in_millis()
    counter = 1
    if webelement:
        while not element_is_interactable and not is_time_out(start_time, 10):
            try:
                webelement.click()
                element_is_interactable = True
            except (ElementNotInteractableException, ElementClickInterceptedException) as e:
                counter = counter + 1
    return element_is_interactable


def get_current_time_in_millis():
    return 10000


def is_time_out(start_time_millis, waiting_interval_seconds):
    return start_time_millis + waiting_interval_seconds * 1000


def elementRef(locatorIdentity):
    if locatorIdentity == 'apclass':
        locatorIdentity = AppiumBy.CLASS_NAME
    if locatorIdentity == 'apacid':
        locatorIdentity = AppiumBy.ACCESSIBILITY_ID
    if locatorIdentity == 'apid':
        locatorIdentity = AppiumBy.ID
    if locatorIdentity == 'apxpath':
        locatorIdentity = AppiumBy.XPATH
    if locatorIdentity == 'class':
        locatorIdentity = By.CLASS_NAME
    if locatorIdentity == 'css':
        locatorIdentity = By.CSS_SELECTOR
    if locatorIdentity == 'id_':
        locatorIdentity = By.ID
    if locatorIdentity == 'xpath':
        locatorIdentity = By.XPATH
    return locatorIdentity
