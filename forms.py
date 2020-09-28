from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email

class MealplanRequestForm(FlaskForm):
    """form to request a mealplan by day or week"""

    timeframe = StringField("Frequency", validators=[InputRequired()])
    target_calorie = IntegerField("Calorie Goal", validators=[InputRequired()])
    diet = SelectField("Dietary Preference", choices = [('none','none'),('vegan','vegan'),('paleo','paleo'),('vegetarian','vegetarin'),('pasctarian','pascatarian')], validators=[InputRequired()])
    excludes = StringField("Excludes", validators=[InputRequired()])
   


