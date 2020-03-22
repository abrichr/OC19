from flask import Blueprint

project_blueprint = Blueprint('project', __name__)


class Project():
    def __init__(self, user, name):
        self.user = user 
        self.name = name


from app.project import routes
