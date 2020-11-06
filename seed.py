from models import User, Project, UserProject,Tasklist, Task, db
from app import app

# create all tables

db.drop_all()
db.create_all()

# drop all tables

User.query.delete()
Project.query.delete()
Tasklist.query.delete()
Task.query.delete()

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

# p1 = Project(name="memory game", technology="html", about="making a 4x4 grid with pictures in it", level="easy", link="http://github.com")

# db.session.add(p1)
# db.session.commit()

# add Project

# up1 = UserProject(project_id=1, username="johnv")
# db.session.add(up1)
# db.session.commit()

# t1 = Task(title="make html", notes="html marker", status="done", project_id=p1.id)

# db.session.add(t1)
# db.session.commit()




