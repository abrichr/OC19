from flask import render_template

from app.home import home_blueprint
from app.project.routes import get_project_views


@home_blueprint.route('/')
def main():
    project_views = get_project_views()
    return render_template('home/main.html', project_views=project_views)
