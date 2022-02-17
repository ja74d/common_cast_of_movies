import requests
from flask import Flask
from bs4 import BeautifulSoup

source = requests.get('https://www.imdb.com/title/tt0816692/fullcredits/?ref_=tt_cl_sm').text
soup = BeautifulSoup(source, 'lxml')

for cast in soup.find_all('tr', class_='odd'):
    
    name = cast.find_all('td')[1].text
    print(name)
    
    role = cast.find('td', class_="character").text
    print(role)