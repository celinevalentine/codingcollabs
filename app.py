from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Mealplan
from forms import MealplanRequestForm
import requests
from secrets import API_Key, Host_Key


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mealplans'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
 
debug = DebugToolbarExtension(app)
 
connect_db(app)
db.create_all()


def get_mealplans_info():
    """generate weekly meal plans for vegetarians"""

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/mealplans/generate"

    querystring = {"timeFrame":"week","targetCalories":"2000","diet":"vegetarian","exclude":"shellfish%2C olives"}

    headers = {
    'x-rapidapi-host': Host_Key,
    'x-rapidapi-key': API_Key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text

# @app.route('/mealplans')
# def get_mealplans():
#     """get meal plans, validating input and returning info about meal plans"""

#     return request.json
   
    
#     form = MealplanRequestForm


#     if form.validate_on_submit():
#         meals = received['properties'][0]['meals'][1]['items'][1]['properties']

   


