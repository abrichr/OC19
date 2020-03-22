from flask import render_template, redirect, request, url_for
from flask_login import login_required
from bson.objectid import ObjectId


from app import mongo
from app.project import project_blueprint
from app.project.forms import SubmitProjectForm


@project_blueprint.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = SubmitProjectForm()
    if request.method == 'POST' and form.validate():
        oid = mongo.db.projects.insert({
            'title': form.title.data,
            'description': form.description.data,
            'needed': form.needed.data,
            'provided': form.provided.data
        })
        return redirect(url_for('project.view', project_id=oid))
    return render_template('project/submit.html', form=form)


@project_blueprint.route('/<project_id>', methods=['GET'])
def view(project_id):
    project = mongo.db.projects.find_one({'_id': ObjectId(project_id)})
    return render_template('project/view.html', project=project)
