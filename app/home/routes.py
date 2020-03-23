import logging

from flask import render_template

from app.home import home_blueprint
from app.project.routes import get_project_views


@home_blueprint.route('/')
def main():
    logging.warning('-=-' * 40)
    logging.warning('warning')
    logging.info('info')
    logging.debug('info')
    project_views = get_project_views()
    return render_template('home/main.html', project_views=project_views)
