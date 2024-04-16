import time

from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

cap: Dict[str, Any] = {
    "platformName": "android",
    "appium:udid": "emulator-5554",
    "deviceName": "Android",
    "appium:appPackage": "io.pharmacyone",
    "appium:appActivity": "io.pharmacyone.landing.presentation.SplashActivity",
    "appium:automationName": "uiautomator2"
}

url = "http://localhost:4724"
driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(cap))

# Get the page source


time.sleep(3)
page_source = driver.page_source
print(page_source)
login_input = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Enter your mobile number"]')
login_input.send_keys("8123456780")
submit_button = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="SUBMIT"]')
submit_button.click()
time.sleep(7)
elements = driver.find_elements(by=AppiumBy.ID, value='io.pharmacyone:id/inputField')
elements[0].send_keys('8')
elements[1].send_keys('8')
elements[2].send_keys('0')
elements[3].send_keys('0')

page_source = driver.page_source
print(page_source)

# Enter your mobile number