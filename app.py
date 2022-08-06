import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from bs4 import BeautifulSoup
import crawler_json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


class MoviesForm(FlaskForm):
    imdb_id1 = StringField('imdb_id1', validators=[DataRequired()])
    imdb_id2 = StringField('imdb_id2', validators=[DataRequired()])
    submit = SubmitField('Submit')

# index
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = MoviesForm()
    if form.validate_on_submit():
        
        imdb_id1 = form.imdb_id1.data
        imdb_id2 = form.imdb_id2.data
        
        url1 = "https://www.imdb.com/title/" + str(imdb_id1) + "/fullcredits/?ref_=tt_cl_sm"
        url2 = "https://www.imdb.com/title/" + str(imdb_id2) + "/fullcredits/?ref_=tt_cl_sm"
        
        source1 = requests.get(url1).text
        source2 = requests.get(url2).text

        soup1 = BeautifulSoup(source1, 'lxml')
        soup2 = BeautifulSoup(source2, 'lxml')

        link_list = []

        fullcast1 = []

        for cast in soup1.find_all('tr', class_='odd') + soup1.find_all('tr', class_='even'):
            
            name = cast.find_all('td')[1].text
            name = name.replace('\n', '')
            link = cast.find_all('td')[1].find('a')['href']
            link = "https://www.imdb.com" + link
            link_list.append(link)
            
            fullcast1.append(name)

        fullcast2 = []

        for cast in soup2.find_all('tr', class_='odd') + soup2.find_all('tr', class_='even'):
            
            name = cast.find_all('td')[1].text
            name = name.replace('\n', '')
            link = cast.find_all('td')[1].find('a')['href']
            link = "https://www.imdb.com" + link
            link_list.append(link)
            
            fullcast2.append(name)

        common_list = []
        

        for i in fullcast1:
            if i in fullcast2:
                common_list.append(i)
        return render_template('index.html', form=form, common_list=common_list, link_list=link_list)

    return render_template('index.html', form=form, common_list=None)

# add json response
@app.route('/<id>', methods=['GET', 'POST'])
def json(id):

    url = "https://www.imdb.com/title/" + str(id) + "/?ref_=tt_mv_close"
    source = requests.get(str(url)).text
    soup = BeautifulSoup(source, 'lxml')

    title = soup.find('h1').text
    year = soup.find('a', class_='ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh').text
    time = soup.find_all('li', class_='ipc-inline-list__item')[5].text
    imdb_rating = soup.find('span', class_='sc-7ab21ed2-1 jGRxWM').text

    poster_lind = soup.find('a', class_='ipc-lockup-overlay ipc-focusable')['href']
    poster_link = "https://www.imdb.com" + poster_lind
    poster_get = requests.get(poster_link).text
    poster_soup = BeautifulSoup(poster_get, 'lxml')
    poster = poster_soup.find('img', class_='sc-7c0a9e7c-0 hXPlvk')['src']

    categories = []
    category = soup.find_all('span', class_='ipc-chip__text')
    for i in category:
        categories.append(i.text)

    story = soup.find('span', class_='sc-16ede01-2 gXUyNh').text
    director = soup.find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link').text

    writers_list = []
    writers = soup.find_all('ul', class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')[1]
    for i in writers.find_all('a'):
        writers_list.append(i.text)

    stars_list = []
    stars = soup.find_all('ul', class_='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')[2]
    for i in stars.find_all('a'):
        stars_list.append(i.text)
    #print(stars_list)

    story_line = soup.find('div', class_='ipc-html-content-inner-div').text

    #casts = soup.find('div', class_='ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-sub-grid--4-unit-at-s ipc-shoveler__grid')
    #cast = casts.find_all('div', class_='sc-36c36dd0-6 ewJBXI')
    #for i in cast:
    #    print(i.text)

    casts_link = soup.find_all('a', class_='ipc-title ipc-title--section-title ipc-title--base ipc-title--on-textPrimary ipc-title-link-wrapper')[1]['href']
    casts_link = "https://www.imdb.com" + casts_link

    casts_get = requests.get(casts_link).text
    casts_soup = BeautifulSoup(casts_get, 'lxml')
    casts = []
    for cast in casts_soup.find_all('tr', class_='odd') + casts_soup.find_all('tr', class_='even'):
                name = cast.find_all('td')[1].text
                name = name.replace('\n', '')
                casts.append(name)

    details = soup.find('div', class_='sc-f65f65be-0 ktSkVi')
    release_date = details.find_all('li', class_='ipc-inline-list__item')[1].text

    return jsonify({

        'title': title, 
        'year': year, 
        'time': time, 
        'imdb_rating': imdb_rating, 
        'poster': poster, 
        'categories': categories, 
        'story': story, 
        'director': director, 
        'writers': writers_list, 
        'stars': stars_list, 
        'story_line': story_line, 
        'casts': casts, 
        'release_date': release_date
        
        })