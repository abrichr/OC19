from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import html_params

from app import mongo


class MyStringField(StringField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = u'is-invalid'

    def __call__(self, *args, **kwargs):
        if self.errors:
            c = kwargs.pop('class', '')
            kwargs['class'] = u'{} {}'.format(self.error_class, c)
        return super().__call__(*args, **kwargs)


class SubmitProjectForm(FlaskForm):
    title = MyStringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    needed = TextAreaField('What do you need?')
    provided = TextAreaField(
        'What can you provide? (e.g. time, money, connections, expertise)'
    )

    def validate_title(form, field):
        project = mongo.db.projects.find_one({'title': field.data}) 
        if project:
            raise ValidationError('Name already exists')
