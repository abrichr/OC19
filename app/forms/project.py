from wtforms.validators import ValidationError
from wtforms_alchemy import ModelForm

from app.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project

    def validate_title(form, field):
        project = Project.query.filter_by(title=field.data).first()
        print(
            'ProjectForm.validate_title() field.data:', field.data,
            'project:', project
        )
        # set in project.routes.edit()
        if project and project.id != form.__dict__.get('_project_id'):
            raise ValidationError('Name already exists')
