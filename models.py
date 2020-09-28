from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
 
db = SQLAlchemy()

class Mealplan(db.Model):
   """mealplan"""

   __tablename__ = "mealplans"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   timeframe = db.Column(db.Text, nullable=False)
   target_calorie = db.Column(db.Integer, nullable=False)
   diet = db.Column(db.Text, nullable=False)
   excludes = db.Column(db.Text, nullable=False)


   








def connect_db(app):
   """Connect to database."""
 
   db.app = app
   db.init_app(app)
