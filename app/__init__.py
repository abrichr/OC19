import os
from pprint import pformat

from flask import Flask, flash, redirect, request, url_for


app = Flask(__name__)

is_debug = bool(int(os.environ.get('DEBUG')))
print('is_debug:', is_debug)
app.debug = is_debug

# Setup the app with the config.py file
app.config.from_object('app.config')

# Setup the logger
from app.logger_setup import logger

# Setup the database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Setup the mail server
from flask_mail import Mail
mail = Mail(app)

# Setup the debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
toolbar = DebugToolbarExtension(app)

# Setup the password crypting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Import the views
from app.views import main, user, project, error
app.register_blueprint(user.userbp)
app.register_blueprint(project.projectbp)

# Setup the user login process
from flask_login import LoginManager
from app.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'


@login_manager.user_loader
def load_user(email):
    user = User.query.filter(User.email == email).first()
    print('load_user() email:', email, 'user:', pformat(vars(user)) if user else '')
    return user


@login_manager.unauthorized_handler
def handle_needs_login():
    flash('You have to be logged in to access this page.' + request.path)
    return redirect(url_for('userbp.signin', next=request.path))


from app import admin
