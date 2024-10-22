import time
import tqdm
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


# get the href links and the episode title
links = []
titles = []
length = 19
driver = get_driver()

for i in tqdm.tqdm(range(length)):
    try:
        url = "https://podscripts.co/podcasts/lions-led-by-donkeys-podcast?page=" + str(length - i)
        driver.get(url)
        time.sleep(2)
        items = driver.find_elements("xpath",
                                     "//div[@class='list-main-wrap fl-wrap card-listing']/div[@class='listing-item']/article[@class='geodir-category-listing fl-wrap']")
    except:
        break
    for item in items:
        link = item.find_element("xpath", ".//a").get_attribute("href")
        title = item.find_element("xpath", ".//h3/a").text
        links.append(link)
        titles.append(title)

print(f"Total episodes: {len(titles)}, Last episode: {titles[-1]}")

pd.DataFrame({"title": titles, "link": links}).to_csv("LLBD.csv", index=False)

driver.close()
driver.quit()
