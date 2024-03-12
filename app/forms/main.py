from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class MainForm(FlaskForm):
    study = StringField("Study", [DataRequired()])
    db_file_path = StringField("DB file path", [DataRequired()])
    remember_path = BooleanField("Remember path")
    submit = SubmitField("Get data")
