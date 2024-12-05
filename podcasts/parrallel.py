import concurrent
import os
# print the current path
import time
import tqdm
import random
import pandas as pd
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore

thread_num = 1
Favs_only = True
def get_wait_time(quick=True):
    if quick:
        return random.uniform(3, 4)
    else:
        return random.uniform(30, 60)

def get_driver():
    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    time.sleep(get_wait_time())
    return driver

def download_mp3(driver, podcast, title, url, semaphore):
    # first check if the podcast folder exists and the mp3 file is not already downloaded
    if os.path.exists(f"/podcasts/downloads/{podcast}/{title}.mp3"):
        return
    with semaphore:
        # try:
        # os.chdir("podcasts/downloads")
        if not os.path.exists(podcast):
            os.makedirs(podcast)
        os.chdir(podcast)
        passed, attempts = False, 0
        while not passed and attempts < 3:
            try:
                driver.get(url)
                passed = True
            except ConnectionError:
                time.sleep(300)
                attempts += 1
        time.sleep(3)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        # time.sleep(2)
        # //*[@id="main_pod_player_parent"]
        # //*[@id="main_pod_player"]
        # /html/body/div/div[3]/div/section/div/div[3]/div/div/div/div[3]/audio/source
        # /html/body/div[1]/div[3]/div/section/div/div[4]/div/div/div/div[3]/audio/source
        mp3 = driver.find_element("xpath", "/html/body/div[1]/div[3]/div/section/div/div[4]/div/div/div/div[3]/audio/source")
        mp3_url = mp3.get_attribute("src")
        bad_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
        for char in bad_chars:
            title = title.replace(char, "")
        if mp3_url not in ["", None]:
            # print(f"Downloading {title}...")
            urllib.request.urlretrieve(mp3_url, f"{title}.mp3")
    # except Exception as e:
    #     print(f"Error downloading {title}: {e}")

def scraper(pods = None):
    if pods is None:
        if not Favs_only:
            pods = pd.read_csv("podscripts.csv")
        else:
            pods = pd.read_csv("podscripts_favs.csv")
    print(f'Starting download of {len(pods)} podcasts')
    semaphore = Semaphore(thread_num)  # Limit to x number of threads
    drivers = [get_driver() for _ in range(thread_num)]
    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        futures = [
            executor.submit(download_mp3, drivers[i % thread_num], pods["podcast"][i], pods["title"][i], pods["link"][i], semaphore)
            for i in range(len(pods))
        ]
        for future in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            future.result()

    # Close drivers after all downloads are complete
    for driver in drivers:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    scraper()