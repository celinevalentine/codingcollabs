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
    img_url = db.Column(db.String, default='/static/images/profile.png')

    recipes = db.relationship('Recipe', secondary = "users_recipes", backref='users')

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
    
    @classmethod
    def default_image(cls):
        return './static/images/profile.png'

    def serialize(self):
        """ Serialize User instance for JSON """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'img_url': self.img_url
        }

    def __repr__(self):
        return f'<User: {self.username}>'

class UserRecipe(db.Model):
    """Many to Many relationship between User and Recipe"""

    __tablename__ = "users_recipes"

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True)
    username = db.Column(db.String, db.ForeignKey('users.username',ondelete='CASCADE'), primary_key=True)

class Recipe(db.Model):
    """Recipe Model"""
    
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    sourceName = db.Column(db.String)
    sourceUrl = db.Column(db.String)
    readyInMinutes = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    instructions = db.Column(db.String)
    vegetarian = db.Column(db.Boolean, default=False)
    vegan = db.Column(db.Boolean, default=False)
    glutenFree = db.Column(db.Boolean, default=False)
    dairyFree = db.Column(db.Boolean, default=False)
    sustainable = db.Column(db.Boolean, default=False)
    ketogenic = db.Column(db.Boolean, default=False)
    whole30 = db.Column(db.Boolean, default=False)

    ingredients = db.relationship(
        "Ingredient", secondary="measurements", backref="recipes")
    steps = db.relationship("Step", backref='recipe')

    
    class Measurement(db.Model):
        """ Many to Many Recipes to Ingredients """
        __tablename__ = "measurements"

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        ingredient_id = db.Column(db.Integer, db.ForeignKey(
            'ingredients.id'))
        recipe_id = db.Column(db.Integer, db.ForeignKey(
            'recipes.id'))
        amount = db.Column(db.Float)
        unit = db.Column(db.String)

        recipe = db.relationship('Recipe', backref='measurements')
        ingredient = db.relationship("Ingredient", backref='measurements')

        def show_measurement(self):
            """ Returns a string with the full measurement """
            return f"{int(self.amount)} {self.unit} {self.ingredient.name}"

    class Ingredient(db.Model):
        """ Ingredient Model """
        __tablename__ = 'ingredients'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, nullable=False, unique=True)
        original = db.Column(db.String)

    
    class Step(db.Model):
        """ Step Model """

        __tablename__ = 'steps'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        recipe_id = db.Column(db.Integer, db.ForeignKey(
            'recipes.id'))
        number = db.Column(db.Integer)
        step = db.Column(db.String)

        def show_step(self):
            """ returns a string of the step number and instructions """
            return f"{self.number}. {self.step}"
   