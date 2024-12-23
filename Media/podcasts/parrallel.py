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
    if os.path.exists(f"/{podcast}/{title}.mp3") or os.path.exists("/{title}.mp3"):
        return
    with semaphore:
        if os.path.basename(os.getcwd()) != podcast:

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

        ''' 
        <div id="main_pod_player_parent" class="pod-player sticky">
        <audio controls="controls" id="main_pod_player">
        <source src="https://chrt.fm/track/138C95/prfx.byspotify.com/e/play.podtrac.com/
        npr-510355/traffic.megaphone.fm/NPR7566169301.mp3?d=645&amp;size=10326144&amp;
        e=1220579287&amp;t=podcast&amp;p=510355"></audio></div>
        '''
        try:
            mp3 = driver.find_element("xpath", "//audio[@id='main_pod_player']/source")
            mp3_url = mp3.get_attribute("src")
            bad_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
            for char in bad_chars:
                title = title.replace(char, "")
            if mp3_url not in ["", None]:
                file_name = f"{title}.mp3"
                if not os.path.exists(file_name):
                    urllib.request.urlretrieve(mp3_url, file_name)

        # except Exception as e:
        except:
            # print(f"Error downloading {title}: {e}")
            pass


def scraper(pods=None, driver=None):
    if pods is None:
        if not Favs_only:
            pods = pd.read_csv("podscripts.csv")
        else:
            pods = pd.read_csv("podscripts_favs.csv")
    print(f'Starting download of {len(pods)} podcasts')
    semaphore = Semaphore(thread_num)  # Limit to x number of threads
    if driver is None:
        drivers = [get_driver() for _ in range(thread_num)]
    else: # it's just thread_num - 1
        drivers = [driver] + [get_driver() for _ in range(thread_num - 1)]

    with ThreadPoolExecutor(max_workers=thread_num) as executor:
        futures = [
            executor.submit(download_mp3, drivers[i % thread_num], pods["podcast"][i], pods["title"][i],
                            pods["link"][i], semaphore)
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
