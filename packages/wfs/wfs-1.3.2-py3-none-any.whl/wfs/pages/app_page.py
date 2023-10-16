import time
from time import sleep
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from cdxg.logging import log
from cdxg.appium_lab.switch import Switch
from poium import Page, Elements, Element

from appium.webdriver.common.touch_action import TouchAction


def get_switch_web(lpage, wcontext=None):
    try:
        # if item == 'sweb':
        lpage = lpage.get_appium_lab()
        if wcontext is None:
            wcontext = lpage.context()
        lpage.switch_to_web(wcontext)
        return wcontext
    except Exception as e:
        return ' Error : on Switch web'


def get_current_context(lpage):
    return lpage.get_appium_lab().context()


def get_switch_back(lpage):
    lpage.get_appium_lab().switch_to_app()
    return 'Swtich back'


def get_tap_swipe(lpage, item, ax, ay):
    AppiumLab = lpage.get_appium_lab()
    if item == 'SwipeUp':
        AppiumLab.swipe_up()
    elif item == 'SwipeDn':
        AppiumLab.swipe_down()
    else:
        if item == 'tap':
            AppiumLab.tap(x=ax, y=ay)
    return 'Tap and Swipe'


def get_key_text(lpage, item, ktext=None):
    AppiumLab = lpage.get_appium_lab()
    if item == 'atype':
        AppiumLab.key_text(ktext)
    if item == 'home':
        AppiumLab.home()
    if item == 'back':
        AppiumLab.back()
    if item == 'kshown':
        ret = AppiumLab.is_keyboard_shown()
    if item == 'hkboard':
        AppiumLab.hide_keyboard()
    if item == 'size':
        size = AppiumLab.size()

    return f"{item} all done clicked"


def getAndroid(lpage, item, greadyx, desc):
    AppiumLab = lpage.get_appium_lab()
    locator_identity, element_identity, action_item, fetchlements = greadyx
    global gclick
    gcn = 'Y'
    timeout_start = time.time()
    timeout = 2 * 15
    progress_net = None
    while not progress_net:
        delta = time.time() - timeout_start
        try:
            if item == 'aclick':
                if gcn == 'Y' and '.View' in element_identity:
                    gclick = AppiumLab.find_view(text=desc)
                    if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                        gcn = 'N'
                    else:
                        progress_net = 'Done'
                if gcn == 'Y' and '.EditText' in element_identity:
                    gclick = AppiumLab.find_edit_text(text=desc)
                    if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                        gcn = 'N'
                    else:
                        gcn = 'Y'
                        progress_net = 'Done'
                if gcn == 'Y' and '.Button' in element_identity:
                    gclick = AppiumLab.find_button(text=desc)
                    if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                        gcn = 'N'
                    else:
                        gcn = 'Y'
                        progress_net = 'Done'
                if gcn == 'Y' and '.TextView' in element_identity:
                    gclick = find_text_view(lpage=lpage, text=desc, greadyx=greadyx)
                    if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                        gcn = 'N'
                    else:
                        gcn = 'Y'
                        progress_net = 'Done'
                if gcn == 'Y' and '.ImageView' in element_identity:
                    gclick = AppiumLab.find_image_view(text=desc)
                    if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                        gcn = 'N'
                    else:
                        gcn = 'Y'
                        progress_net = 'Done'
                if gcn == 'Y' and '.CheckBox' in element_identity:
                    gclick = AppiumLab.find_check_box(text=desc)
                    if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                        gcn = 'N'
                    else:
                        gcn = 'Y'
                        progress_net = 'Done'
                if gcn == 'Y' and '.Button' in element_identity:
                    gclick = AppiumLab.find_button(content_desc=desc)
                    if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                        gcn = 'N'
                    else:
                        gcn = 'Y'
                        progress_net = 'Done'
                if gcn == 'Y' and '.View' in element_identity:
                    gclick = AppiumLab.find_view(content_desc=desc)
                    if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                        gcn = 'N'
                    else:
                        gcn = 'Y'
                        progress_net = 'Done'

                if gcn == 'Y' and item == 'aclick':
                    gclick.click()
                    gcn = ' Action Clicked Done...'
                else:
                    gcn = 'Error : ' + str(gclick)
        except Exception as e:
            gcn = 'Error : ' + str(e)

        if progress_net == 'Done':
            progress_net = 'Success'
        if delta >= timeout:
            break
    return gcn


def getiOS(lpage, item, greadyx, desc):
    AppiumLab = lpage.get_appium_lab()
    locator_identity, element_identity, action_item, fetchlements = greadyx
    global gclick
    gcn = 'Y'
    if item == 'aclick':
        if gcn == 'Y' and 'TypeStaticText' in element_identity:
            gclick = AppiumLab.find_static_text(text=desc)
            if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                gcn = 'N'
        if gcn == 'Y' and 'TypeOther' in element_identity:
            gclick = AppiumLab.find_other(text=desc)
            if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                gcn = 'N'
            else:
                gcn = 'Y'
        if gcn == 'Y' and 'TypeTextField' in element_identity:
            gclick = AppiumLab.find_text_field(text=desc)
            if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                gcn = 'N'
            else:
                gcn = 'Y'
        if gcn == 'Y' and 'TypeImage' in element_identity:
            gclick = AppiumLab.find_image(text=desc)
            if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                gcn = 'N'
            else:
                gcn = 'Y'
        if gcn == 'Y' and 'TypeButton' in element_identity:
            gclick = AppiumLab.find_ios_button(text=desc)
            if gclick in [f"Unable to find -> {desc}", "parameter error, setting text/content_desc"]:
                gcn = 'N'
            else:
                gcn = 'Y'

        if gcn == 'Y' and item == 'aclick':
            gclick.click()
            gcn = ' Action Clicked Done...'
            gcn = 'Error : ' + str(gclick)
        return gcn


def remove_unprintable_chars(string: str) -> str:
    """
    remove unprintable chars
    :param string: string
    """
    print('93289028wejhwkjhskdsds-------------1')
    return ''.join(x for x in string if x.isprintable())


def find(lpage, attribute: str, text: str):
    """
    find element
    :param class_name: class name
    :param attribute: attribute
    :param text: text
    :return:
    """

    # elems = lpage.find_elements(AppiumBy.CLASS_NAME, class_name)
    # elems = Elements.find(AppiumBy.CLASS_NAME, class_name)
    elems = lpage

    for _ in range(3):
        if len(elems) > 0:
            break
        sleep(1)

    for elem in elems:
        if elem.get_attribute(attribute) is None:
            continue
        attribute_text = remove_unprintable_chars(elem.get_attribute(attribute))
        if text in attribute_text:
            log.info(f'find -> {attribute_text}')
            return elem
    return None


def find_text_view(lpage, text, greadyx):
    """
    Android: find TextView
    :param text:
    :return:
    """
    lpage = lpage.locators_ready(greadyx=greadyx)
    # get_switch_back(lpage)
    for _ in range(3):
        elem = find(lpage, attribute="text", text=text)
        if elem is not None:
            break
        sleep(1)
    else:
        raise ValueError(f"Unable to find -> {text}")

    return elem


def get_injecta_data(customattribute, customvalue, ptname):
    element_attribute = customattribute
    element_value = customvalue

    if ptname == 'Android':
        # Android
        exename = 'mobile: shell', {
            'command': 'input',
            'args': ['text', f'new UiSelector().description("{element_attribute}={element_value}")']
        }
    else:
        # iOS
        exename = 'mobile: shell', {
            'command': 'input',
            'args': ['text', f'[{element_attribute}="{element_value}"]']
        }

    # Android
    # element = driver.find_element(MobileBy.XPATH, f'//*[@content-desc="{element_attribute}={element_value}"]')
    # iOS
    # element = driver.find_element(MobileBy.XPATH, f'//*[@{element_attribute}="{element_value}"]')
    # Interact with the element
    # element.click()

    return exename
