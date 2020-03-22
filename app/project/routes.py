from flask import render_template
from flask_login import login_required

from app.project import project_blueprint 


@project_blueprint.route('/submit', methods=['POST', 'GET'])
@login_required
def submit():
    return render_template('project/submit.html')
