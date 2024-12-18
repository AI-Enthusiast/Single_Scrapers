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

url = 'https://www.imdb.com/chart/boxoffice/'

