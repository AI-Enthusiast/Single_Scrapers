url = 'https://www.netflix.com/tudum/top10'
import os
import time
import random
import pandas as pd
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager  # pip install webdriver-manager

def get_wait_time(quick=True):
    if quick:
        return random.uniform(2, 4)
    else:
        return random.uniform(30, 60)
def get_driver():  # set up the driver
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    time.sleep(get_wait_time())
    return driver

def get_top_10(url=url):
    driver = get_driver()
    driver.get(url)
    time.sleep(5)
    # .css-baaif4 > svg:nth-child(1)
    # click the dl button
    driver.find_element("css selector", ".css-baaif4 > svg:nth-child(1)").click()
    time.sleep(5)
    # /html/body/div[1]/div/div/div[1]/div/div[2]/section[2]/div/div/div/div/div/dialog/div/div[2]/div/ul/li[2]/button
    # click the list button
    driver.find_element("xpath", "/html/body/div[1]/div/div/div[1]/div/div[2]/section[2]/div/div/div/div/div/dialog/div/div[2]/div/ul/li[2]/button").click()
    time.sleep(get_wait_time())
    # /html/body/div[1]/div/div/div[1]/div/div[2]/section[2]/div/div/div/div/div/dialog/div/div[2]/div/div[2]/div/div[2]/button
    # click the global download button
    driver.find_element("xpath", "/html/body/div[1]/div/div/div[1]/div/div[2]/section[2]/div/div/div/div/div/dialog/div/div[2]/div/div[2]/div/div[2]/button").click()
    time.sleep(get_wait_time())
    # /html/body/div[1]/div/div/div[1]/div/div[2]/section[2]/div/div/div/div/div/dialog/div/div[2]/div/div[2]/div/div[5]/button
    # click the county download button
    driver.find_element("xpath", "/html/body/div[1]/div/div/div[1]/div/div[2]/section[2]/div/div/div/div/div/dialog/div/div[2]/div/div[2]/div/div[5]/button").click()
    time.sleep(get_wait_time())
    # /html/body/div[1]/div/div/div[1]/div/div[2]/section[2]/div/div/div/div/div/dialog/div/div[2]/div/div[2]/div/div[8]/button
    # click the popular download button
    driver.find_element("xpath", "/html/body/div[1]/div/div/div[1]/div/div[2]/section[2]/div/div/div/div/div/dialog/div/div[2]/div/div[2]/div/div[8]/button").click()
    time.sleep(get_wait_time())

    driver.quit()

get_top_10()