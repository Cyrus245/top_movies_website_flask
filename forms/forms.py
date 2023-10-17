from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired


class EditForm(FlaskForm):
    rating = FloatField("Your Rating Out of 10 e.g. 7.5", [DataRequired()])
    review = StringField("Your Review", [DataRequired()])
    submit = SubmitField("Done")