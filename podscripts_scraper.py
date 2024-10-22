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


pods = ['lions-led-by-donkeys-podcast',
        'behind-the-bastards',
        'stuff-you-should-know',
        'my-favorite-murder-with-karen-kilgariff-and-georgia-hardstark',
        'last-podcast-on-the-left',
        'the-dollop-with-dave-anthony-and-gareth-reynolds',
        'crime-junkie']


def build_url(pod_name, page):
    url_prefix = "https://podscripts.co/podcasts/"
    url_suffix = "?page="
    return url_prefix + pod_name + url_suffix + str(page) if page > 1 else url_prefix + pod_name


driver = get_driver()
output = []  # podcast, title, link
old_len = 0
for podcast in pods:
    pod_pretty = podcast.replace('-', ' ').title()
    more_pages = True
    page = 1
    len_change = 0
    while more_pages:
        try:
            driver.get(build_url(podcast, page))
            time.sleep(get_wait_time())
            items = driver.find_elements("xpath",
                                         "//div[@class='list-main-wrap fl-wrap card-listing']/div[@class='listing-item']/article[@class='geodir-category-listing fl-wrap']")

        except:
            more_pages = False
            break
        for item in items:
            link = item.find_element("xpath", ".//a").get_attribute("href")
            title = item.find_element("xpath", ".//h3/a").text
            output.append([pod_pretty, title, link])
        if len_change == len(output):
            more_pages = False
        len_change = len(output)

        page += 1

    print(f"Total episodes for {pod_pretty}: {len(output) - old_len}")
    old_len = len(output)

pd.DataFrame(output, columns=["podcast", "title", "link"]).to_csv("podscripts.csv", index=False)

driver.close()

import dl_pod
