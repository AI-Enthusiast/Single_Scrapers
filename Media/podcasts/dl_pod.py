import os
import time
import tqdm
import random
import pandas as pd
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager  # pip install webdriver-manager


def get_wait_time(quick=True):
    if quick:
        return random.uniform(4, 9)
    else:
        return random.uniform(30, 60)


def get_driver():  # set up the driver
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    time.sleep(get_wait_time())
    return driver

driver = get_driver()

# open LLBD.csv
pods = pd.read_csv("podscripts.csv")

for i in tqdm.tqdm(range(len(pods))):
    title = pods["title"][i]
    url = pods["link"][i]
    podcast = pods["podcast"][i]

    # change location to downloads
    # /home/cormac/DataspellProjects/Single_Scrapers/downloads
    os.chdir("/downloads")
    # create a folder for the podcast if it doesn't exist
    if not os.path.exists(podcast):
        os.makedirs(podcast)
    # change location to the podcast folder
    os.chdir(podcast)

    driver.get(url)

    time.sleep(1)
    # scroll mid
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    time.sleep(2)

# /html/body/div[1]/div[3]/div/section/div/div[3]/div/div/div/div[3]/audio/source

    mp3 = driver.find_element("xpath", "/html/body/div[1]/div[3]/div/section/div/div[3]/div/div/div/div[3]/audio/source")
    print(mp3)
    print(mp3.get_attribute("src"))
    mp3_url = mp3.get_attribute("src")
    if mp3_url not in ["", None]:
        print("Downloading...")
        import urllib.request

        urllib.request.urlretrieve(mp3_url, f"{title}.mp3")

# import urllib.request
#
# urllib.request.urlretrieve(mp3, f"{title}.mp3")

driver.close()