from flask import flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required
from bson.objectid import ObjectId


from app import mongo
from app.project import project_blueprint
from app.project.forms import SubmitProjectForm


@project_blueprint.route('/submit/', methods=['GET', 'POST'])
@login_required
def submit():
    form = SubmitProjectForm()
    is_valid = form.validate()
    was_submitted = request.method == 'POST'
    print('project.submit() form:', form, 'is_valid:', is_valid)
    if was_submitted:
        if is_valid:
            project_dict = {
                'title': form.title.data,
                'description': form.description.data,
                'needed': form.needed.data,
                'provided': form.provided.data,
                'user_id': current_user.id
            }
            print('project.submit() project_dict:', project_dict)
            result = mongo.db.projects.insert_one(project_dict)
            inserted_id = result.inserted_id
            return redirect(url_for('project.view', project_id=inserted_id))
        else:
            flash('There was an error with your submission, please try again')
    return render_template(
        'project/submit.html',
        form=form,
        is_invalid=(not is_valid) and was_submitted
    )


@project_blueprint.route('/join/<project_id>/', methods=['GET', 'POST'])
@login_required
def join(project_id):
    # TODO: join current user to project
    return redirect(url_for('project.view', project_id=project_id))


@project_blueprint.route('/<project_id>/', methods=['GET'])
def view(project_id):
    project = mongo.db.projects.find_one({'_id': ObjectId(project_id)})
    return render_template('project/view.html', project=project)


def get_project_views():
    projects = mongo.db.projects.find()
    # TODO: augment with owner, subscribers
    return projects
