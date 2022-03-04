import json
import time
import datetime

from calendar import monthrange

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Date for synchronization 
currentDateTime = datetime.datetime.now()
year = int(currentDateTime.year)
month = int(currentDateTime.month)
day = int(currentDateTime.day)
unused_first_day_or_whatever, actual_month_days = monthrange(year, month)

# Variables and other items used in crucial functions
shifts = []
shift = {}
shifts_planned_upwards = 14
table_item_xpath = '/html/body/div[2]/div[3]/div[2]/div/table[1]/tbody/tr[3]/td[{0}]/div[{1}]'

# Information to log in
f = open('login.json')
login = json.load(f)
f.close

# Set path for Selenium
CHROMIUM_PATH = '/bin/chromium-browser'
s = Service(CHROMIUM_PATH)
driver = webdriver.Chrome()

# Function that simplifies the getting shifts data function
def gettingTableData(starting_day, ammount_of_days):

    for i in range(starting_day + 1, ammount_of_days):

            shift = {
                'day': i - 1,
                'start': driver.find_element(By.XPATH, table_item_xpath.format(i, 1)).text,
                'end': driver.find_element(By.XPATH, table_item_xpath.format(i, 2)).text,
                'note': driver.find_element(By.XPATH, table_item_xpath.format(i, 3)).text
            }
            shifts.append(shift)

# Function to get shifts two weeks upfront
def gettingTheMonthlyData(days_in_the_month, day):
    
    if days_in_the_month - day >= shifts_planned_upwards:

        gettingTableData(day, shifts_planned_upwards)

    else:

        days_left_in_month = days_in_the_month - day
        days_left = shifts_planned_upwards - days_left_in_month

        gettingTableData(day, days_left_in_month)
        driver.get("https://mymcd.eu/app/CZ019/#/shifts/{0}-{1}/".format(year, month + 1))
        time.sleep(1)
        gettingTableData(day, days_left_in_month)

    with open('shifts.json', 'w', encoding='utf-8') as f:
        json.dump(shifts, f, ensure_ascii=False, indent=4)

# Login section
driver.get("https://mymcd.eu/login/")
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(login[0])
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(login[1])
driver.find_element(By.XPATH, '/html/body/div[1]/form/div[2]/input[2]').click()

# Getting the shifts data
driver.get("https://mymcd.eu/app/CZ019/#/shifts/")
time.sleep(10)
gettingTheMonthlyData(actual_month_days, day)
driver.close()