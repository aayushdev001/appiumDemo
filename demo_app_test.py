from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

cap: Dict[str, Any] = {
    "platformName": "android",
    "appium:udid": "emulator-5554",
    "deviceName": "Android",
    "appium:appPackage": "com.hmh.api",
    "appium:appActivity": "com.hmh.api.ApiDemos",
    "appium:automationName": "uiautomator2"
}

url = "http://localhost:4724"
driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(cap))

el = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Continue"]')
el.click()

# driver.quit()
# "platformName": "android",
#   "appium:udid": "emulator-5554",
#   "appium:appPackage": "com.hmh.api",
#   "appium:appActivity": "com.hmh.api.ApiDemos",
#   "appium:automationName": "uiautomator2"