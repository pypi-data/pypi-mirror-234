import os.path as ph
from pathlib import Path
from appium import webdriver
from selenium.common.exceptions import WebDriverException
from configparser import ConfigParser

mypath = Path.cwd()
cObject = ConfigParser()
cObject.read('conf.ini')

LOCAL_HOST = cObject.get('MobileHost', 'local_host')  # 'http://localhost:4723/wd/hub'
CURRENT_DEVICE = cObject.get('MobileHost', 'android_current_device_pax')  # 'emulator-5554'
# PLATFORM_NAME =  cObject.get('MobileHost', 'platform_name')  # 'Android'
APP_PATH_APK_DRV = cObject.get('MobileHost', 'local_host')  # ph.join(ph.dirname(__file__), 'Driverapp.apk')
APP_PATH_APK_PAX = cObject.get('MobileHost', 'local_host')  # ph.join(ph.dirname(__file__), 'ShopFront.apk')

print('***********************************')
print(APP_PATH_APK_DRV, APP_PATH_APK_PAX)
print('*************************************')


def restart_pax_session(driver):
    try:
        # Quit the current session
        driver.quit()
    except WebDriverException:
        # Handle any exceptions if the session is already terminated
        pass

    # Start a new session
    desired_caps = {
        'deviceName': CURRENT_DEVICE,
        'platformName': 'Android',
        'app': APP_PATH_APK_PAX,
        'noReset': True
        # Add other desired capabilities as needed
    }
    driver = webdriver.Remote(LOCAL_HOST, desired_caps)
    return driver


def restart_drv_session(driver):
    try:
        # Quit the current session
        driver.quit()
    except WebDriverException:
        # Handle any exceptions if the session is already terminated
        pass

    # Start a new session
    desired_caps = {
        'deviceName': CURRENT_DEVICE,
        'platformName': 'Android',
        'app': APP_PATH_APK_DRV,
        'noReset': True
        # Add other desired capabilities as needed
    }
    driver = webdriver.Remote(LOCAL_HOST, desired_caps)
    return driver


def drv_session(ptname, boolx=True):
    # Start a new session

    fpath = mypath / 'test_data' / 'mobile' / 'apps'
    if ptname == 'Android':
        drvfile = cObject.get('MobileHost', 'android_app_path_driver')
        APP_PATH_APK_DRV = fpath / drvfile
        print(APP_PATH_APK_DRV)
        desired_caps = {
            'deviceName': cObject.get('MobileHost', 'android_current_device_drv'),
            # 'udid': cObject.get('MobileHost', 'android_current_device_drv'),
            'platformName': ptname,
            'app': str(APP_PATH_APK_DRV),
            'noReset': boolx,
            "autoGrantPermissions": True,
            "autoAcceptAlerts": True,
            'videoRecordingEnabled': True
            # Add other desired capabilities as needed
        }
    else:
        drvfile = cObject.get('MobileHost', 'ios_app_path_driver')
        APP_PATH_IPA_DRV = fpath / drvfile
        desired_caps = {
            'deviceName': cObject.get('MobileHost', 'ios_current_device'),
            'platformName': ptname,
            'app': str(APP_PATH_IPA_DRV),
            'noReset': boolx,
            "autoGrantPermissions": True,
            "autoAcceptAlerts": True,
            'videoRecordingEnabled': True
            # Add other desired capabilities as needed
        }
    driver = webdriver.Remote(LOCAL_HOST, desired_caps)
    return driver


def pax_session(ptname, boolx=True):
    # Start a new session
    fpath = mypath / 'test_data' / 'mobile' / 'apps'
    if ptname == 'Android':
        paxfile = cObject.get('MobileHost', 'android_app_path_pax')
        APP_PATH_APK_PAX = fpath / paxfile
        print(APP_PATH_APK_PAX)
        desired_caps = {
            'deviceName': cObject.get('MobileHost', 'android_current_device_pax'),
            # 'udid': cObject.get('MobileHost', 'android_current_device_pax'),
            'platformName': ptname,
            'app': str(APP_PATH_APK_PAX),
            'noReset': boolx,
            "autoGrantPermissions": True,
            "autoAcceptAlerts": True,
            'videoRecordingEnabled': True
            # Add other desired capabilities as needed
        }
    else:
        paxfile = cObject.get('MobileHost', 'ios_app_path_pax')
        APP_PATH_IPA_PAX = fpath / paxfile
        desired_caps = {
            'deviceName': cObject.get('MobileHost', 'ios_current_device'),
            'platformName': ptname,
            'app': str(APP_PATH_IPA_PAX),
            'noReset': boolx,
            "autoGrantPermissions": True,
            "autoAcceptAlerts": True,
            'videoRecordingEnabled': True
            # Add other desired capabilities as needed
        }
    driver = webdriver.Remote(LOCAL_HOST, desired_caps)
    return driver
