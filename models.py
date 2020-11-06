from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
   """Connect to database."""
 
   db.app = app
   db.init_app(app)

class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    apods = db.relationship('APOD', secondary = "users_apods", backref='users')

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a user and generate hashed password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
    
class UserApod(db.Model):
    """Many to Many relationship between User and Launch"""

    __tablename__ = "users_apods"

    id = db.Column(db.Integer, db.ForeignKey('apods.id', ondelete='CASCADE'), primary_key=True)
    username = db.Column(db.String, db.ForeignKey('users.username',ondelete='CASCADE'), primary_key=True)

class APOD(db.Model):
    """APOD Model"""
    
    __tablename__ = "apods"

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String)
    date = db.Column(db.DateTime)
    hdurl = db.Column(db.String)
    explanation = db.Column(db.String)