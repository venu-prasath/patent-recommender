import os
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.by import By
import pandas as pd



opts = ChromeOptions()
opts.add_experimental_option("detach", True)

os.environ['PATH'] += r"D:/installed/chrome_driver/chrome-win64"
driver = Chrome(options=opts)

driver.get("https://patents.google.com/")
title = driver.title
driver.implicitly_wait(1)

# text_box = driver.find_element(by=By.NAME, value="my-text")
# submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
#
# text_box.send_keys("Selenium")
# submit_button.click()
#
# message = driver.find_element(by=By.ID, value="message")
# text = message.text
# print(text)

search_input = driver.find_element(by=By.CSS_SELECTOR, value="#searchInput")
search_input.send_keys("Machine Learning")

search_button = driver.find_element(by=By.CSS_SELECTOR, value="#searchButton")
search_button.click()

driver.implicitly_wait(2)
#first search item for test
items = driver.find_elements(By.CSS_SELECTOR, "search-result-item state-modifier a")
print("Items length: ", len(items))

for item in items:
    link = item.get_attribute("href")
    print(link)

items[0].click()
abstract = driver.find_element(By.CSS_SELECTOR, "#abstract patent-text")
