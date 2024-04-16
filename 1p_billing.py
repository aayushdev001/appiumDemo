import re
import time

from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

cap: Dict[str, Any] = {
    "platformName": "android",
    "appium:udid": "emulator-5554",
    "appium:deviceName": "Android",
    "appium:appPackage": "io.pharmacyone",
    "appium:appActivity": "io.pharmacyone.landing.presentation.SplashActivity",
    "appium:automationName": "uiautomator2",
    "appium:ensureWebviewsHavePages": True,
    "appium:nativeWebScreenshot": True,
    "appium:newCommandTimeout": 3600,
    "appium:connectHardwareKeyboard": True
}

url = "http://localhost:4724"
driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(cap))
wait = WebDriverWait(driver, 20)

# Get the page source


time.sleep(3)
page_source = driver.page_source
# print(page_source)

# login page
login_input = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Enter your mobile number"]')
login_input.send_keys("8123456780")
submit_button = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="SUBMIT"]')
submit_button.click()
time.sleep(7)

# otp page
elements = driver.find_elements(by=AppiumBy.ID, value='io.pharmacyone:id/inputField')
elements[0].send_keys('8')
elements[1].send_keys('8')
elements[2].send_keys('0')
elements[3].send_keys('0')

# home page
time.sleep(8)
sales_button = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.FrameLayout[@content-desc=\"Sales\"]")
sales_button.click()

# billing page
time.sleep(3)
new_sales_button = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="New Sale"]')
new_sales_button.click()

# new bill page
time.sleep(5)
product_input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'android.widget.EditText')))
product_input.click()
time.sleep(4)
product_search = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//android.widget.EditText')))
time.sleep(4)
product_search.click()
product_search.send_keys("Dolfin")
time.sleep(3)
add_button = driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Add"]')
add_button.click()
time.sleep(3)

# batch name
try:
    strip_loose_toggle = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="O"]')
except NoSuchElementException:
    strip_loose_toggle = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@text="I"]')
strip_loose_toggle.click()

default_batch_name = driver.find_element(by=AppiumBy.XPATH,
                                         value="//android.widget.TextView[contains(@text, 'Batch "
                                               "Number')]/following-sibling::*").text

# stock
# available_stock_exp = driver.find_element(by=AppiumBy.XPATH, value="//*[contains(text(), 'Batch Stock')]").text
available_stock_exp = wait.until(
    EC.presence_of_element_located((By.XPATH, "//android.widget.TextView[contains(@text, 'Batch Stock:')]")))
pattern = r'\d+$'
match = re.search(pattern, available_stock_exp.text)
if match:
    number = int(match.group())
    print("Available stock:", number)
else:
    print("Stock error")

# MRP
mrp = float(driver.find_element(by=AppiumBy.XPATH,
                                value="//android.widget.TextView[contains(@text, 'MRP (₹)')]/following-sibling::*").text)
print("MRP: ", mrp)

# Discount
discount = float(driver.find_element(by=AppiumBy.XPATH,
                                     value="//android.widget.TextView[contains(@text, 'Discount ("
                                           "%)')]/following-sibling::*").text)
print("Discount: ", discount)

# Quantity
quantity = driver.find_element(by=AppiumBy.XPATH,
                               value="//android.widget.TextView[contains(@text, 'Quantity')]/following-sibling::*")
quantity.clear()
quantity.send_keys("13")

#Done
done_button = driver.find_element(by=AppiumBy.XPATH,
                                  value="//android.widget.TextView[contains(@text, 'Done')]")
done_button.click()

# actual total
actual_total = driver.find_element(by=AppiumBy.XPATH,
                                   value="//android.widget.TextView[contains(@text, 'Quantity')]/following-sibling::*")
actual_total = actual_total.text.replace('₹', '').strip()
expected_total = mrp * 13 * (1 - discount / 100)
print("Expected total: ", expected_total)
print("Actual total: ", actual_total)

# submit bill
proceed_button = driver.find_element(by=AppiumBy.XPATH,
                                     value="//android.widget.TextView[contains(@text, 'Proceed')]")
proceed_button.click()
time.sleep(6)

permission_access = driver.find_element(by=AppiumBy.XPATH,
                                        value="//android.widget.Button[contains(@text, 'While using the app')]")
permission_access.click()
time.sleep(2)

# submit_button = driver.find_element(by=AppiumBy.XPATH,
#                                         value="//android.widget.TextView[@text, 'Submit']")
submit_button = driver.find_element(by=AppiumBy.XPATH,
                                        value='//android.widget.TextView[@text="Submit"]')
submit_button.click()

# bill history

driver.press_keycode(4)
latest_bill = driver.find_elements(by=AppiumBy.XPATH, value="//android.widget.TextView[contains(@text, 'Bill')]")
latest_bill[1].click()
time.sleep(4)
medicine_link = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.TextView[contains(@text, 'Dolfin')]")
medicine_link.click()
time.sleep(2)

# medicine inventory
remaining_stock = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.TextView[contains(@text, 'Total Stock')]")
pattern = r'Stock: (\d+):'
match = re.search(pattern, remaining_stock.text)
if match:
    extracted_number = match.group(1)
    print("Extracted number:", extracted_number)
else:
    print("No number found between 'Stock' and the next colon ':'.")
