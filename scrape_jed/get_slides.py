# Author: Cormac Dacker (cdacker@willamette.edu)
# Date: 2024-01-23
import pandas as pd
import os
import time
import requests
import selenium.common.exceptions
from PIL import Image  # pip install pillow
from selenium import webdriver  # pip install selenium
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager  # pip install webdriver-manager
root = os.path.dirname(os.path.realpath('get_slides.py'))

from selenium.common.exceptions import ElementClickInterceptedException

def get_slides(url, path, driver):
    wait_time = 3  # seconds
    if url is None:
        url = input('Enter the url of the first slide: ')

    # get the title of the slides
    title = url.split('/')[-1].split('.')[0]
    pdf_path = root + path + '/slides/' + title + '.pdf'
    # check if the pdf already exists
    if os.path.exists(pdf_path):
        print('Slides already exist for ' + title)
        return

    print('Scraping slides for ' + title)

    # create a folder for the slides
    try:  # create a folder for the slides
        os.mkdir(root + path + '/slides')
    except FileExistsError:
        pass
    try:  # create a folder for these slides
        os.mkdir(root + path + '/slides/' + title)
    except FileExistsError:
        pass
    # print(url)
    try:
        driver.get(url)
    except selenium.common.exceptions.TimeoutException:
        print('Timed out, retrying...')
        time.sleep(300) # wait 5 minutes
        driver.get(url)
    # scrape the slides until there are no more slides, screenshot each slide
    broken = False
    slide = 1
    while not broken:
        time.sleep(wait_time)
        try:
            driver.save_screenshot(root + path + '/slides/' + title + '/' + str(slide) + '.png')  # screenshot the slide
            # Hide the slide number element
            driver.execute_script("document.querySelector('.slide-number').style.display='none';")
            # hide the title footer
            driver.execute_script("document.querySelector('#title-footer').style.display='none';")
            # check if click down is an option before clicking right
            # /html/body/div[3]/aside/button[4]/div
            try:
                driver.find_element("xpath", "/html/body/div[3]/aside/button[4]").click() # click down
                slide += 1
                continue
            except:
                pass
            driver.find_element("xpath", "/html/body/div[3]/aside/button[2]/div").click() # click right
            slide += 1
        except ElementClickInterceptedException:
            print('Element click intercepted, retrying...')
            time.sleep(wait_time)
        except:
            broken = True
            print('Finished scraping slides')

    # get all file in the slides folder
    files = os.listdir(root + path + '/slides/' + title + '/')
    files.sort(key=lambda x: os.path.getmtime(root + path + '/slides/' + title + '/' + x))

    # compile the slides into a pdf
    images = []
    for x in files:
        png = Image.open(root + path + '/slides/' + title + '/' + x)
        png.load()  # required for png.split()
        background = Image.new("RGB", png.size, (255, 255, 255))
        background.paste(png, mask=png.split()[3])  # 3 is the alpha channel
        images.append(background)

    images[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
    print('Saved slides to ' + pdf_path.split('/')[-1])

    # delete the slides from the slides folder
    for file in files:
        os.remove(root + path + '/slides/' + title + '/' + file)
    os.rmdir(root + path + '/slides/' + title)  # delete the folder

def get_all_slides():
    # set up the driver
    options = Options()
    options.headless = True  # don't trust the user to not mess with the slides
    driver = webdriver.Firefox(options=options)
    time.sleep(1)

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
    # print(csv_list)
    # ['/home/user/DataspellProjects/Single_Scrapers/scrape_jed/classes/Data_Management_with_SQL/Data_Management_with_SQL.csv', '/home/user/DataspellProjects/Single_Scrapers/scrape_jed/classes/Intro_to_Programming_with_Python/Intro_to_Programming_with_Python.csv']
    # get the name of the dir that the csv is in
    class_name = [csv.split('/')[-2] for csv in csv_list]
    i= 0
    for jed_class in csv_list:
        df = pd.read_csv(jed_class)
        for index, row in df.iterrows():
            slide_link = row['link']
            slide_link = 'https://jrembold.github.io/' + slide_link
            get_slides(slide_link, '/classes/' + class_name[i], driver)
        i += 1
    driver.quit()

get_all_slides()