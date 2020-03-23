from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


app = Flask(__name__)

app.config.from_pyfile('config.py')
app.secret_key = os.urandom(24)

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

from app.home import home_blueprint
app.register_blueprint(home_blueprint)

from app.project import project_blueprint
app.register_blueprint(project_blueprint, url_prefix='/project')

from app.admin import admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

login_manager.login_view = "user.login"


@app.context_processor
def inject_app_name():
    return dict(app_name='OC19')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
