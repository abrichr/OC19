from flask import Blueprint


home_blueprint = Blueprint('home', __name__)


from app.home import routes
