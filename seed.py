from models import User, Post, db
from app import app

db.create_all()


u1 = User(username="johnv", password="johnv", email="jv@gmail.com", first_name="john", last_name="val")

db.session.add(u1)
db.session.commit()

p1 = Post(topic="mars", summary="By 2021, USA will launch a first spaceship to Mars!", image_url="https://unsplash.com/photos/NR_tXTuyTak", username="johnv")

db.session.add(p1)
db.session.commit()