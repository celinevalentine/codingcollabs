from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email, Length, URL, NumberRange, Optional, DataRequired
from wtforms.fields.html5 import DateField, URLField

class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired()],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)],
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)],
    )
    img_url = URLField('Profile Image URL(optional)', validators =[Optional()])

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class UserEditForm(FlaskForm):
    """Form for editing a user."""
    
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
