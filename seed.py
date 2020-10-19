from models import User, Project, UserProject,Task, db
from app import app

db.drop_all()
db.create_all()

u1 = User(username="johnv", password="$2b$12$C1WEsfPRZUpl2nE3CvqQF.HiOz1ZwyauP1sLjb6KiobCdqeo8u/9a", email="jv@gmail.com", first_name="john", last_name="val")

db.session.add(u1)
db.session.commit()

p1 = Project(name="memory game", technology="html", about="making a 4x4 grid with pictures in it", level="easy", link="http://github.com")

db.session.add(p1)
db.session.commit()

up1 = UserProject(project_id=1, username="johnv")
db.session.add(up1)
db.session.commit()

t1 = Task(title="make html", notes="html marker", status="done", project_id=p1.id)

db.session.add(t1)
db.session.commit()




