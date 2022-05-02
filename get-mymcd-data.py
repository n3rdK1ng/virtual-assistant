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

# Selenium Set-Up
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('--log-level=3')
driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)
driver.set_window_size(1920,1080)

# Function that simplifies the getting shifts data function
def gettingTableData(starting_day, ammount_of_days, month, year):

    time.sleep(10)

    for i in range(starting_day + 1, starting_day + ammount_of_days + 2):
          
        gday = i - 1
        start = driver.find_element(By.XPATH, table_item_xpath.format(i, 1)).text
        startx = start[:-3]
        starty = start[-2:]
        end = driver.find_element(By.XPATH, table_item_xpath.format(i, 2)).text
        endx = end[:-3]
        endy = end[-2:]
        note = driver.find_element(By.XPATH, table_item_xpath.format(i, 3)).text
        
        # In case there's a nightshift
        try:
            if int(startx) > int(endx):
                night = 1
            else:
                night = 0
        except:
            pass

        if start != "":

            shift = {
                'summary': 'Work',
                'location': 'Francouzská 5, 708 00 Ostrava-Poruba',
                'description': note,
                'start': {
                    'dateTime': f'{year}-{month}-{gday}T{startx}:{starty}:00+02:00',
                    'timeZone': 'Europe/Prague',
                },
                'end': {
                    'dateTime': f'{year}-{month}-{gday + night}T{endx}:{endy}:00+02:00',
                    'timeZone': 'Europe/Prague',
                },
                'reminders': {
                    'useDefault': bool(False),
                    'overrides': [
                        {'method': 'popup', 'minutes': 60},
                    ],
                },                
            }
            shifts.append(shift)

# Function to get shifts two weeks upfront
def gettingTheMonthlyData(days_in_the_month, day):
    
    if days_in_the_month - day >= shifts_planned_upwards:

        gettingTableData(day, shifts_planned_upwards, month, year)

    else:

        days_left_in_month = days_in_the_month - day
        days_left = shifts_planned_upwards - days_left_in_month

        gettingTableData(day, days_left_in_month, month, year)
        driver.get("https://mymcd.eu/app/CZ019/#/shifts/{0}-{1}/".format(year, month + 1))

        if month + 1 == 13:
            gettingTableData(1, days_left - 1, 1, year + 1)
        else:
            gettingTableData(1, days_left - 1, month + 1, year)

    with open('shifts.json', 'w', encoding='utf-8') as f:
        json.dump(shifts, f, ensure_ascii=False, indent=4)

# Login section
driver.get("https://mymcd.eu/login/")
driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(login[0])
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(login[1])
driver.find_element(By.XPATH, '/html/body/div[1]/form/div[2]/input[2]').click()

# Getting the shifts data
driver.get("https://mymcd.eu/app/CZ019/#/shifts/")
gettingTheMonthlyData(actual_month_days, day)
driver.quit()