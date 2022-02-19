import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from bs4 import BeautifulSoup


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

        fullcast1 = []

        for cast in soup1.find_all('tr', class_='odd') + soup1.find_all('tr', class_='even'):
            
            name = cast.find_all('td')[1].text
            name = name.replace('\n', '')
            fullcast1.append(name)

        fullcast2 = []

        for cast in soup2.find_all('tr', class_='odd') + soup2.find_all('tr', class_='even'):
            
            name = cast.find_all('td')[1].text
            name = name.replace('\n', '')
            fullcast2.append(name)

        common_list = []

        for i in fullcast1:
            if i in fullcast2:
                common_list.append(i)
        return render_template('index.html', form=form, common_list=common_list)

    return render_template('index.html', form=form, common_list=None)