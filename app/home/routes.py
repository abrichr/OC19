from flask import render_template

from app.home import home_blueprint


@home_blueprint.route('/')
def main():
    return render_template('home/main.html')
