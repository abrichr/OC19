from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from app import mongo


class SubmitProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    needed = TextAreaField('What do you need?')
    provided = TextAreaField(
        'What can you provide? (e.g. time, money, connections, expertise)'
    )

    def validate_title(form, field):
        project = mongo.db.projects.find_one({'title': field.data}) 
        if project:
            raise ValidationError('Name already exists')
