# TODO: move this to app/views/admin.py

import os.path as op

from flask import request, Response
from werkzeug.exceptions import HTTPException
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from app import app, db, config
from app.models import User, Project, Comment


print('config.env_path:', config.env_path)


admin = Admin(app, name='Admin', template_mode='bootstrap3')

class ModelView(ModelView):
    def is_accessible(self):
        auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
        if (
            not auth or
            (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']
        ):
            raise HTTPException(
                '',
                Response(
                    'You have to bean administrator.',
                    401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'}
                )
            )
        return True


class UserView(ModelView):
    column_hide_backrefs = False


class ProjectView(ModelView):
    column_hide_backrefs = False


class CommentView(ModelView):
    column_hide_backrefs = False


# Users
admin.add_view(UserView(User, db.session))
admin.add_view(ProjectView(Project, db.session))
admin.add_view(CommentView(Comment, db.session))

# Static files
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static'))
