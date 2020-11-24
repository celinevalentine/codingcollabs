from models import db, User
from app import app

# create all tables

db.drop_all()
db.create_all()

# create User

u1 = User(username="john", password="password", email="jv@gmail.com", first_name="john", last_name="v", img_url='/static/images/profile.png')

db.session.add_all(u1)
db.session.commit()

