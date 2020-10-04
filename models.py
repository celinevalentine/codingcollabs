from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
 
db = SQLAlchemy()

class User(db.Model):
    """User"""

    __tablename__ = "users"

    username = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    posts = db.relationship("Post", backref="user", cascade="all, delete")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a user, hashing their password."""

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

class Post(db.Model):
    """Post"""
    
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)
    image_url = db.Column(
        db.String, nullable=False)
    username = db.Column(db.String,db.ForeignKey('users.username'), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
      'Post',
      secondary="posts_tags",
      cascade="all,delete",
      backref="tags",
    )

class Comment(db.Model):
    """Comment."""

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(10),
        db.ForeignKey('users.username'),
        nullable=False,
    )


def connect_db(app):
   """Connect to database."""
 
   db.app = app
   db.init_app(app)
