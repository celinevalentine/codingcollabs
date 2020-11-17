from models import db, User, Recipe
import requests
from secrets import API_Key


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

    url = f"{BASE_URL}/recipes/search"
    querystring = generate_search_params()
    headers = generate_headers()

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()

def get_recipe(id):

    url = f"{BASE_URL}/recipes/{id}/information"
    headers = generate_headers()
    response = requests.request("GET", url, headers=headers, data={"apiKey":API_Key, "id":id})

    return response

def get_visual_ingredients(id):
    """Visualize recipe ingredients by id"""
    url = f"{BASE_URL}/recipes/{id}/ingredientWidget"
    
    headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': API_Key,
    'accept': "text/html"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)

    return response.text


def get_visual_nutrition():
    """Visualize recipe nutrition facts by id"""

    url = f"{BASE_URL}/recipes/{id}/nutritionWidget"

    headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': API_Key,
    'accept': "text/html"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)
    return response.text

def get_visual_taste():
    """Visualize recipe taste by id"""

    url = f"{BASE_URL}/recipes/{id}/visualizeTaste"

    headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': API_Key,
    'accept': "text/html"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)
    return response.text

def create_recipe_card():
    """Make a recipe card from favorites"""

    url = f"{BASE_URL}/recipes/{id}/visualizeRecipe"

    payload = ""
    headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': API_Key,
    'content-type': "multipart/form-data"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    return response.text


def add_commit_db(obj):
    """Add and commit an object to the db, then return obj"""
    db.session.add(obj)
    db.session.commit()
    return obj

def add_recipe_db(data):
    """Add a recipe to db then return the recipe from db"""
    id = data.get('id', None)
    title = data.get('title', None)
    image = data.get('image', None)
    sourceName = data.get('sourceName', None)
    sourceUrl = data.get('sourceUrl', None)
    readyInMinutes = data.get('readyInMinutes', None)
    servings = data.get('servings', None)
    instructions = data.get('instructions', None)
    vegetarian = data.get('vegetarian', None)
    vegan = data.get('vegan', None)
    glutenFree = data.get('glutenFree', None)
    dairyFree = data.get('dairyFree', None)
    sustainable = data.get('sustainable', None)
    ketogenic = data.get('ketogenic', None)
    whole30 = data.get('whole30', None)

    recipe = Recipe(id=id, title=title, image=image, sourceName=sourceName, sourceUrl=sourceUrl,
                    readyInMinutes=readyInMinutes, servings=servings, instructions=instructions, vegetarian=vegetarian, vegan=vegan, glutenFree=glutenFree, dairyFree=dairyFree, sustainable=sustainable, ketogenic=ketogenic, whole30=whole30)
    try:
        recipe = add_and_commit(recipe)
    except Exception:
        db.session.rollback()
        print(str(Exception))
        return "Recipe couldn't be saved. Please try again."

    ingredients = add_ingredients_to_db(recipe_data)
    for ingredient in ingredients:
        recipe.ingredients.append(ingredient)
        db.session.commit()

    return recipe 


def add_ingredients_to_db(recipe_data):
    """ 
    Add ingredients and measurements to the db
    recipe_data (obj)"""
    ingredient_list = []
    for ingredient in recipe_data['extendedIngredients']:
    
        db_ingredient = Ingredient.query.filter_by(
        id=ingredient['id']).first()
        if db_ingredient:
            ingredient_list.append(db_ingredient)
        else:
            id = ingredient.get('id', None)
            name = ingredient.get('name', None)
            original = ingredient.get('original', None)

            new_ingredient = Ingredient(
                id=id, name=name, original=original)

            new_ingredient = add_and_commit(new_ingredient)
            print(f"\n Created new ingredient {new_ingredient} \n")

            ingredient_list.append(new_ingredient)
            print(f"\n Ingredient added to list: {ingredient_list} \n")

            recipe_data = add_measurement_for_ingredient(
            ingredient, recipe_data)
        return ingredient_list


def add_measurement_for_ingredient(ingredient, recipe_data):
    """
    Add measurements for corresponding ingredients in a recipe to the db 
    """
  
    recipe_id = recipe_data.get('id', None)
    ingredient_id = ingredient.get('id', None)
    amount = ingredient.get('amount', None)
    unit = ingredient.get('unit', None)
    new_measurement = Measurement(
        ingredient_id=ingredient_id, recipe_id=recipe_id, amount=amount, unit=unit)
    new_measurement = add_and_commit(new_measurement)

    return recipe_data

