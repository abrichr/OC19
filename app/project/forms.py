from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from app import mongo


class SubmitProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    needed = TextAreaField('What do you need?')
    provided = TextAreaField(
        'What can you provide? (e.g. time, money, connections, expertise)'
    )
    contact = TextAreaField(
        'How should team members collaborate? '
        '(e.g. organizer\'s email address, '
        '<a href="https://slack.com/create">Slack</a>, '
        '<a href="https://trello.com/signup">Trello</a>'
    )

    def validate_title(form, field):
        project = mongo.db.projects.find_one({'title': field.data}) 
        # set in project.routes.edit()
        if project and str(project['_id']) != form.__dict__.get('_project_id'):
            raise ValidationError('Name already exists')
