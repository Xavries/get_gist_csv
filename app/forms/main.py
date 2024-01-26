from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired

from app.models import Study
from app import db


class MainForm(FlaskForm):
    study = StringField("Study", [DataRequired()])
    submit = SubmitField("Get data")
