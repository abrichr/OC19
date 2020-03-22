from flask import Blueprint
from flask_login import UserMixin

from app import bcrypt


user_blueprint = Blueprint('user', __name__)


class User(UserMixin):
    def __init__(self, email, name, can_invite_users=False):
        self.email = email
        self.name = name
        self.can_invite_users = can_invite_users

    @staticmethod
    def is_authenticated(self):
        self.authenticated = True

    def get_id(self):
        return self.email

    @staticmethod
    def validate_login(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)


from app.user import routes
