from models import User, APOD, UserApod,db
from secrets import APOD_API
import requests
from flask import request



BASE_URL = "https://api.nasa.gov"

def get_apod(search_date):
    """Make API call for all apods."""

    search_date = request.args['search']

    url = f"{BASE_URL}/planetary/apod"

    querystring = {"date":f"{search_date}","hd":"False","api_key": APOD_API}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring)

    data = response.json()

    title = data['title']
    date = data['date']
    hdurl = data['hdurl']
    explanation = data['explanation']

    apod = {
            'title': title,
            'date': date,
            'hdurl': hdurl,
            'explanation': explanation
            }
            
    return apod


def load_new_apod():

    db.drop_all()
    db.create_all()

    search_date = request.form['search']

    data = get_apod(search_date)

    new_apod = APOD(
        title=title,
        date=date,
        hdurl=hdurl,
        explanation=explanation)
    
    db.session.add(new_apod)
    db.session.commit()
 




