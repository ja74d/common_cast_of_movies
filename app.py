import requests
from flask import Flask
from bs4 import BeautifulSoup


imdb_id1 = 'tt0468569'
imdb_id2 = 'tt1345836'

url1 = "https://www.imdb.com/title/" + str(imdb_id1) + "/fullcredits/?ref_=tt_cl_sm"
url2 = "https://www.imdb.com/title/" + str(imdb_id2) + "/fullcredits/?ref_=tt_cl_sm"

source1 = requests.get(url1).text
source2 = requests.get(url2).text

soup1 = BeautifulSoup(source1, 'lxml')
soup2 = BeautifulSoup(source2, 'lxml')

fullcast1 = []

for cast in soup1.find_all('tr', class_='odd') + soup1.find_all('tr', class_='even'):
    
    name = cast.find_all('td')[1].text
    name = name.replace('\n', '')
    fullcast1.append(name)
    #print(name)
    
    #role = cast.find('td', class_="character").text
    #print(role)
#print(fullcast1)

fullcast2 = []

for cast in soup2.find_all('tr', class_='odd') + soup2.find_all('tr', class_='even'):
    
    name = cast.find_all('td')[1].text
    name = name.replace('\n', '')
    fullcast2.append(name)
    #print(name)
    
    #role = cast.find('td', class_="character").text
    #print(role)
#print(fullcast2)

common_list = set(fullcast1).intersection(fullcast2)

print(common_list)