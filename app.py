from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Mealplan
from forms import MealplanRequestForm
import requests
from secrets import API_Key


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mealplans'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
 
debug = DebugToolbarExtension(app)
 
connect_db(app)
db.create_all()

API_BASE_URL = "https://api.nasa.gov"

def pic_of_day():
    """get a picture of the day from NASA"""

  
    response = requests.get(f"{API_BASE_URL}/planetary/apod")
    r = resopnse.json() 
    return r['date']

    

@app.route('/')
def homepage():
    
    response = requests.get(f"{API_BASE_URL}/planetary/apod")
    r = response.json()['title']
    date = request.args['date']
  

    
    return render_template('index.html', date = date, title=title)








   


