from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, URL, NumberRange

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

class PostForm(FlaskForm):
    """Add post form."""
    topic = StringField(
        "What is your research topic?",
        validators=[InputRequired(), Length(max=30)],
    )
    summary = TextAreaField(
        "Summarize your research in 150- 250 words.",
        validators=[InputRequired(), Length(max=150)]
    )
    image_url = StringField(
        "Upload one best image url (see instructions)",
        validators=[InputRequired(), URL()]
    )

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""




