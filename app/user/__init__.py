from flask import Blueprint
from flask_login import UserMixin

from app import bcrypt, mongo, login_manager


user_blueprint = Blueprint('user', __name__)


class User(UserMixin):
    def __init__(
        self,
        email,
        name,
        password_hash=None,
        can_invite_users=False,
        can_create_projects=False
    ):
        print('User', locals())
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.can_invite_users = can_invite_users
        self.can_create_projects = can_create_projects

    @staticmethod
    def is_authenticated(self):
        self.authenticated = True

    def get_id(self):
        return self.email

    @staticmethod
    def validate_login(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)


@login_manager.user_loader
def load_user(email, user_dict=None):
    if not user_dict:
        user_dict = mongo.db.users.find_one({'email': email})
    print('load_user() user_dict:', user_dict)
    if not user_dict:
        return None
    return User(
        email=user_dict['email'],
        name=user_dict['name'],
        can_invite_users=user_dict['can_invite_users'],
        can_create_projects=user_dict['can_create_projects'],
        password_hash=user_dict['password']
    )


from app.user import routes
