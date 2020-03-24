from bson.objectid import ObjectId
from flask import Blueprint
from flask_login import UserMixin

from app import app, bcrypt, mongo, login_manager


user_blueprint = Blueprint('user', __name__)


class User(UserMixin):
    def __init__(
        self,
        _id,
        email,
        name,
        password_hash=None,
        is_superadmin=False
    ):
        print('User', locals())
        self.id = _id
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.project_ids = self._get_project_ids()
        self.is_superadmin = is_superadmin

    @staticmethod
    def is_authenticated(self):
        self.authenticated = True

    def get_id(self):
        return self.email

    @staticmethod
    def validate_login(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)

    def can_edit_project(project_id):
        return self.is_superadmin or project_id in self.project_ids

    def _get_project_ids(self):
        project_ids = set()
        result = mongo.db.projects.find({
            'user_id': ObjectId(self.id)
        })
        for project in result:
            project_id = str(project['_id'])
            print('User.project_ids project_id:', project_id)
            project_ids.add(project_id)
        return project_ids


@login_manager.user_loader
def load_user(email, user_dict=None):
    if not user_dict:
        user_dict = mongo.db.users.find_one({'email': email})
    print('load_user() user_dict:', user_dict)
    if not user_dict:
        return None
    return User(
        _id=user_dict['_id'],
        email=user_dict['email'],
        name=user_dict['name'],
        is_superadmin=user_dict['is_superadmin'],
        password_hash=user_dict['password']
    )


from app.user import routes
