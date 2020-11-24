from models import db, User, Recipe
import requests
from os import API_Key


BASE_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"

def valid_cuisines():
    return ['african', 'chinese', 'japanese', 'korean', 'vietnamese', 'thai', 'indian', 'british', 'irish', 'french', 'italian', 'mexican',
                  'spanish', 'middle eastern', 'jewish', 'american', 'cajun', 'southern', 'greek', 'german', 'nordic', 'eastern european', 'caribbean', 'latin american']
def valid_diets():
    return ['lacto vegetarian','ovo vegetarian', 'vegan', 'vegetarian']

def generate_headers():
    """ Returns headers """
    return {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': API_Key
    }
def generate_search_params(query=None, cuisine=None, diet=None, offset=0, number=10):
    return {
        "apiKey": API_Key,
        "query": query,
        "diet": diet,
        "cuisine": cuisine,
        "offset": offset,
        "number": number
    }


def search_recipes(request):

    query = request.args.get("query","")
    cuisine = request.args.get("cuisine","")
    diet = request.args.get("diet","")
    offset = int(request.args.get("offset",0))
    number=10

    url = f"{BASE_URL}/recipes/search"
    querystring = generate_search_params(query,cuisine,diet,offset,number)
    headers = generate_headers()

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()

def get_recipe(id):

    url = f"{BASE_URL}/recipes/{id}/information"
    headers = generate_headers()
    response = requests.request("GET", url, headers=headers, data={"apiKey":API_Key, "id":id})

    return response.json()





