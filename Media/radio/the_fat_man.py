import os
import time
import tqdm
import random
import pandas as pd
import urllib.request
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

def check_radio_broadcasts(path):
    os.chdir(path)
    urls = [
        'https://www.radioechoes.com/?page=series&genre=OTR-Detective&series=The%20Fat%20Man',
            'https://www.radioechoes.com/?page=series&genre=OTR-Detective&series=The%20Thin%20Man',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=The%20Sound%20Of%20War',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201800s',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201900',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201901',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201902',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201903',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201904',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201905',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201906',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201907',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201908',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201909',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201910',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201911',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201912',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201913',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201914',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201915',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201916',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201917',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201918',
            'https://www.radioechoes.com/?page=series&genre=OTR-Historical&series=Early%20Recordings%20Circa%201919']

    driver = get_driver()

    for url in urls:
        driver.get(url)

        # create a folder for the podcast if it doesn't exist
        podcast = url.split("series=")[1].replace('%20', ' ')
        if not os.path.exists(podcast):
            os.makedirs(podcast)

        # find all div class="episodeWrapper"
        episodes = driver.find_elements("xpath", "//div[@class='episodeWrapper']")
        # print(len(episodes))

        # for each episode, get the title and the download link
        # class="episodeTitle"
        # class="downloadEpisode"
        row = []  # title, link, dl_title, dl_date
        for episode in episodes:
        # for episode in tqdm.tqdm(episodes, desc=f"Downloading {podcast}"):
            title = episode.find_element("class name", "episodeTitle").text
            # <div class="downloadEpisode"><a href="?page=play_download&amp;mode=download&amp;dl_mp3folder=T&amp;dl_file=the_fat_man_1946-01-21_the_19th_pearl.mp3&amp;dl_series=The Fat Man&amp;dl_title=The 19th Pearl&amp;dl_date=1946.01.21&amp;dl_size=6.67 MB" title="Download Episode">Download Episode</a> - <span class="fileDetails">File Size:6.67 MB</span></div>
            link = episode.find_element("class name", "downloadEpisode").find_element("tag name", "a").get_attribute("href")
            dl_date = link.split("dl_date=")[1].split("&")[0]
            dl_date = dl_date.replace(".", "-")
            file_name = f"{podcast}/{title} ({dl_date}).mp3"

            # check if the file is already downloaded
            if not os.path.exists(file_name):
                row.append([link, file_name])

        download = pd.DataFrame(row, columns=["link", "file_name"])

        # open each link and click the download button
        # <div class="downloadLink"><a href="https://s3.amazonaws.com/RE-Warehouse/t/the_fat_man_1946-01-21_the_19th_pearl.mp3" download="https://s3.amazonaws.com/RE-Warehouse/t/the_fat_man_1946-01-21_the_19th_pearl.mp3">Download MP3 file</a></div>
        # for link, file_name in row:
        for i, row in tqdm.tqdm(download.iterrows(), total=len(download), desc=f"Downloading {podcast}"):
            link, file_name = row["link"], row["file_name"]
            driver.get(link)
            time.sleep(2)
            mp3_url = driver.find_element("class name", "downloadLink").find_element("tag name", "a").get_attribute("href")
            time.sleep(2)

            urllib.request.urlretrieve(mp3_url, file_name)

    driver.close()
    driver.quit()