from models import User
from app import app

# create all tables

db.drop_all()
db.create_all()

# drop all tables

User.query.delete()


# create User

u1 = User(username="john", password="password", email="jv@gmail.com", first_name="john", last_name="v", bio='software engineer student', location='Miami,FL',profile_image_url='User.profile_image_url.default.arg')

nancyv_data = {
    'username': 'nancyv',
    'password': 'vnancy',
    'first_name': 'nancy',
    'last_name':'val',
    'email': 'nv@test.com'
    
}

nancyv = User.register(nancyv_data)

db.session.add_all(u1,nancyv)
db.session.commit()

