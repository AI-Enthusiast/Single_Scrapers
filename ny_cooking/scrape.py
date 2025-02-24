import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import re
import json
import pandas as pd4
import time
import random


def get_wait_time(lower_bound=3, upper_bound=6):
    return random.uniform(lower_bound, upper_bound)


def get_driver():  # set up the driver
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    time.sleep(get_wait_time())
    return driver


# Set up the driver, with user agent to avoid detection
driver = webdriver.Firefox()
prefix = 'https://cooking.nytimes.com/'  # +{recipe_id}
driver.get(prefix)
time.sleep(get_wait_time())  # wait for the page to load

# accept the terms and conditions
#
# accept_button = driver.find_element('', '')
time.sleep(get_wait_time())  # wait for the page to load

# click the 'login' button
# using the xpath /html/body/div/div/header/div[1]/div[2]/nav/span/button[1]/span
login_button = driver.find_element('xpath', '/html/body/div/div/header/div[1]/div[2]/nav/span/button[1]/span')
login_button.click()
time.sleep(get_wait_time())  # wait for the page to load

user = ''
password = ''
# it will automaticall put the cursor in the email field
# <input id="email" name="email" type="email" placeholder="" maxlength="64" autocapitalize="none" autocomplete="username" tabindex="0" aria-hidden="false" class="css-11g480x-InputBox e1e6zg665" value="">
email_field = driver.find_element('xpath', '//*[@id="email"]')
email_field.send_keys(user)
time.sleep(get_wait_time(6,10))
email_field.send_keys(Keys.RETURN) # press enter
# now pw
# <input id="password" name="password" type="password" placeholder="" maxlength="255" autocapitalize="none" autocomplete="off" tabindex="0" aria-hidden="false" class="css-e478v4-InputBox e1e6zg665" value="">
pw_field = driver.find_element('xpath', '//*[@id="password"]')
pw_field.send_keys(password)
pw_field.send_keys(Keys.RETURN) # press enter
time.sleep(get_wait_time(8,12))

# now we are logged in goto recipie 10
recipe_id = 10
driver.get(prefix + str(recipe_id))
time.sleep(get_wait_time())
