import requests
from bs4 import BeautifulSoup
import os

#Need to solve login first
r = requests.get('https://mymcd.eu/app/CZ019/#/shifts/2021-12/')
print(r)

soup = BeautifulSoup(r.content, 'html.parser')
print(soup.prettify())