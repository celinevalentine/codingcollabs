from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email, Length, URL, NumberRange, Optional, DataRequired

class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired()],
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

class LoginForm(FlaskForm):
    """login form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class UserEditForm(FlaskForm):
    """Form for editing a user."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    header_image_url = StringField('(Optional) Header Image URL')
    bio = TextAreaField('(Optional) Tell us about yourself')
    password = PasswordField('Password', validators=[Length(min=6)])
class AddProjectForm(FlaskForm):
    """Add project form."""
    name = StringField(
        "Name",
        validators=[InputRequired()],
    )
    technology = StringField(
        "Technology",
        validators=[InputRequired()],
    )
    about = TextAreaField(
        "About",
        validators=[InputRequired()]
    )
    level = SelectField("Level", choices=[('easy','easy'),('intermediate', 'intermediate'),('hard','hard')])
    
    link = StringField(
        "Source Code",
        validators=[InputRequired(), URL()]
    )
    availability = BooleanField("Available")

    
class DeleteForm(FlaskForm):
    """Delete form"""







