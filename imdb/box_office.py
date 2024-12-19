import concurrent
import os
import time
import requests
import tqdm
import random
import pandas as pd
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup

box_office = 'https://www.imdb.com/chart/boxoffice/'

raw = requests.get(box_office, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(raw.text, 'html.parser')


# <div class="ipc-metadata-list-summary-item__tc"><span class="ipc-metadata-list-summary-item__t" aria-disabled="false"></span><div class="sc-300a8231-0 gTnHyA cli-children"><div class="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-a69a4297-2 bqNXEn cli-title with-margin"><a href="/title/tt13622970/?ref_=chtbo_t_1" class="ipc-title-link-wrapper" tabindex="0"><h3 class="ipc-title__text">1. Moana 2</h3></a></div><ul class="sc-8f57e62c-0 eJUTAo sc-300a8231-8 iBYCkW" data-testid="title-metadata-box-office-data-container"><li class="sc-8f57e62c-1 kFGSJM"><span>Weekend Gross<!-- -->: </span><span class="sc-8f57e62c-2 ftiqYS">$26M</span></li><li class="sc-8f57e62c-1 kFGSJM"><span>Total Gross<!-- -->: </span><span class="sc-8f57e62c-2 ftiqYS">$342M</span></li><li class="sc-8f57e62c-1 kFGSJM"><span>Weeks Released<!-- -->: </span><span class="sc-8f57e62c-2 ftiqYS">3</span></li></ul><span class="sc-300a8231-1 kWSYcu"><div class="sc-e2dbc1a3-0 jeHPdh sc-300a8231-3 koIPa cli-ratings-container" data-testid="ratingGroup--container"><span aria-label="IMDb rating: 7.0" class="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating" data-testid="ratingGroup--imdb-rating"><svg width="24" height="24" xmlns="http://www.w3.org/2000/svg" class="ipc-icon ipc-icon--star-inline" viewBox="0 0 24 24" fill="currentColor" role="presentation"><path d="M12 20.1l5.82 3.682c1.066.675 2.37-.322 2.09-1.584l-1.543-6.926 5.146-4.667c.94-.85.435-2.465-.799-2.567l-6.773-.602L13.29.89a1.38 1.38 0 0 0-2.581 0l-2.65 6.53-6.774.602C.052 8.126-.453 9.74.486 10.59l5.147 4.666-1.542 6.926c-.28 1.262 1.023 2.26 2.09 1.585L12 20.099z"></path></svg><span class="ipc-rating-star--rating">7.0</span><span class="ipc-rating-star--voteCount">&nbsp;(<!-- -->43K<!-- -->)</span></span><button aria-label="Rate Moana 2" class="ipc-rate-button sc-e2dbc1a3-1 HRgde ratingGroup--user-rating ipc-rate-button--unrated ipc-rate-button--base" data-testid="rate-button"><span class="ipc-rating-star ipc-rating-star--base ipc-rating-star--rate"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="ipc-icon ipc-icon--star-border-inline" viewBox="0 0 24 24" fill="currentColor" role="presentation"><path d="M22.724 8.217l-6.786-.587-2.65-6.22c-.477-1.133-2.103-1.133-2.58 0l-2.65 6.234-6.772.573c-1.234.098-1.739 1.636-.8 2.446l5.146 4.446-1.542 6.598c-.28 1.202 1.023 2.153 2.09 1.51l5.818-3.495 5.819 3.509c1.065.643 2.37-.308 2.089-1.51l-1.542-6.612 5.145-4.446c.94-.81.45-2.348-.785-2.446zm-10.726 8.89l-5.272 3.174 1.402-5.983-4.655-4.026 6.141-.531 2.384-5.634 2.398 5.648 6.14.531-4.654 4.026 1.402 5.983-5.286-3.187z"></path></svg><span class="ipc-rating-star--rate">Rate</span></span></button></div></span></div></div>
movies = soup.find_all('div', class_='ipc-metadata-list-summary-item__tc')

movie_names = []
for movie in movies:
    movie_names.append(movie.find('h3', class_='ipc-title__text').text)

weekend_gross = []
total_gross = []
weeks_released = []
ratings = []
for movie in movies:
    metadata = movie.find_all('li', class_='sc-8f57e62c-1 kFGSJM')
    weekend_gross.append(metadata[0].find('span', class_='sc-8f57e62c-2 ftiqYS').text)
    total_gross.append(metadata[1].find('span', class_='sc-8f57e62c-2 ftiqYS').text)
    weeks_released.append(metadata[2].find('span', class_='sc-8f57e62c-2 ftiqYS').text)

    ratings.append(movie.find('span', class_='ipc-rating-star--rating').text)

df = pd.DataFrame({'Movie': movie_names, 'Weekend Gross': weekend_gross, 'Total Gross': total_gross, 'Weeks Released': weeks_released, 'Rating': ratings})
df.to_csv('box_office.csv', index=False)

for index, row in df.iterrows():
    print(f'{row["Movie"]}\n\tWeekend Gross: {row["Weekend Gross"]}\n\tTotal Gross: {row["Total Gross"]}\n\tWeeks Released: {row["Weeks Released"]}\n\tRating: {row["Rating"]}\n####')
quit(42)
