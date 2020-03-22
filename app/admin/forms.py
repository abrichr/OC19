from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from app import mongo


class InviteForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
