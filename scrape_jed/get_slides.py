# Author: Cormac Dacker (cdacker@willamette.edu)
# Date: 2024-01-23
import pandas as pd
import os
import time
import requests
from PIL import Image  # pip install pillow
from selenium import webdriver  # pip install selenium
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager  # pip install webdriver-manager
root = os.path.dirname(os.path.realpath('scrape_slides.py'))

def get_slides(url, name=None):
    wait_time = 2  # seconds
    if url is None:
        url = input('Enter the url of the first slide: ')

    # get the title of the slides
    title = url.split('/')[-1].split('.')[0]
    print('Scraping slides for ' + title)

    # create a folder for the slides
    try:  # create a folder for the slides
        os.mkdir(root + '/slides')
    except FileExistsError:
        pass
    try:  # create a folder for these slides
        os.mkdir(root + '/slides/' + title)
    except FileExistsError:
        pass

    # set up the driver
    options = Options()
    options.headless = True  # don't trust the user to not mess with the slides
    driver = webdriver.Firefox(options=options)
    time.sleep(wait_time)
    driver.get(url)

    # scrape the slides until there are no more slides, screenshot each slide
    broken = False
    slide = 1
    while not broken:
        try:
            driver.save_screenshot(root + '/slides/' + title + '/' + str(slide) + '.png')  # screenshot the slide
            # <button class="navigate-right enabled highlight" aria-label="next slide"><div class="controls-arrow"></div></button>
            driver.find_element_by_class_name('navigate-right').click()  # get next slide
            time.sleep(wait_time)
            slide += 1
        except requests.exceptions.ConnectionError:
            print('Connection error')
            time.sleep(wait_time)
        except:
            broken = True
            print('Finished scraping slides')
    driver.close()  # close the driver

    # get all file in the slides folder
    files = os.listdir(root + '/slides/' + title + '/')
    files.sort(key=lambda x: os.path.getmtime(root + '/slides/' + title + '/' + x))

    # compile the slides into a pdf
    images = []
    for x in files:
        png = Image.open(root + '/slides/' + title + '/' + x)
        png.load()  # required for png.split()
        background = Image.new("RGB", png.size, (255, 255, 255))
        background.paste(png, mask=png.split()[3])  # 3 is the alpha channel
        images.append(background)
    pdf_path = root + '/slides/' + title + '.pdf'
    images[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
    print('Saved slides to ' + pdf_path.split('/')[-1])

    # delete the slides from the slides folder
    for file in files:
        os.remove(root + '/slides/' + title + '/' + file)
    os.rmdir(root + '/slides/' + title)  # delete the folder

def get_all_slides():
    # change dir to /classes/
    os.chdir("classes")
    print(os.getcwd())
    # recursively fetch all csvs
    csv_list = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".csv"):
                csv_list.append(os.path.join(root, file))
    print(f'Found {len(csv_list)} classes')
    for jed_class in csv_list:
        df = pd.read_csv(jed_class)
        for index, row in df.iterrows():
            slide_link = row['link']

            get_slides(slide_link)

get_all_slides()