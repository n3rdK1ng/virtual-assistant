import json
import time
import datetime

from calendar import monthrange

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Date for synchronization 
currentDateTime = datetime.datetime.now()
year = int(currentDateTime.year)
month = int(currentDateTime.month)
day = int(currentDateTime.day)

# Information to log in
f = open('login.json')
login = json.load(f)
f.close

# Set path Selenium
CHROMIUM_PATH = '/usr/local/bin/chromium-browser'
s = Service(CHROMIUM_PATH)
WINDOW_SIZE = "1920,1080"

# Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = CHROMIUM_PATH
driver = webdriver.Chrome(options=chrome_options)

# Login section
driver.get("https://mymcd.eu/login/")
driver.find_element_by_xpath('//*[@id="username"]').send_keys(login[0])
driver.find_element_by_xpath('//*[@id="password"]').send_keys(login[1])
driver.find_element_by_xpath('/html/body/div[1]/form/div[2]/input[2]').click()

# Getting the shifts data
driver.get("https://mymcd.eu/app/CZ019/#/shifts/")
time.sleep(1)
actual_month_days = monthrange(year, month)

driver.close()

#Function to get shifts two weeks upfront
#def gettingTheMonthlyData(monthrange, day):
