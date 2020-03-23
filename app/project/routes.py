from flask import abort, flash, render_template, redirect, request, url_for
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
                'contact': form.contact.data,
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


def user_is_in_project(project_id, user_id):
    result = mongo.db.projects.find_one({
        '_id': ObjectId(project_id),
        'users': {
            '$in': [user_id]
        }
    })
    #print('user_is_in_project() result:', result)
    return bool(result)


def toggle_user_in_project(project_id, user_id):
    print('toggle_user_in_project() project_id:', project_id, 'user_id:', user_id)
    if user_is_in_project(project_id, user_id):
        result = mongo.db.projects.update_one({
            '_id': ObjectId(project_id)
        }, {
            '$pull': {
                'users': user_id
            }
        })
        modified_count = result.modified_count
        print('toggle_user_in_project() remove modified_count:', modified_count)
        return -modified_count
    else:
        result = mongo.db.projects.update_one({
            '_id': ObjectId(project_id)
        }, {
            '$addToSet': {
                'users': ObjectId(user_id)
            }
        })
        modified_count = result.modified_count
        print('toggle_user_in_project() add modified_count:', modified_count)
        return modified_count


@project_blueprint.route('/join/<project_id>/', methods=['GET', 'POST'])
@login_required
def join(project_id):
    modified_count = toggle_user_in_project(project_id, current_user.id)
    if modified_count > 0:
        flash('Joined project successfully')
    elif modified_count < 0:
        flash('Left project successfully')
    return redirect(url_for('project.view', project_id=project_id))


@project_blueprint.route('/<project_id>/', methods=['GET'])
def view(project_id):
    print('current_user:', vars(current_user))
    project = mongo.db.projects.find_one({'_id': ObjectId(project_id)})
    if not project:
        return abort(404)
    user_id = project['user_id']
    owner = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return render_template('project/view.html', project=project, owner=owner)


@project_blueprint.route('/delete/<project_id>/', methods=['POST'])
def delete(project_id):
    result = mongo.db.projects.delete_one({'_id': ObjectId(project_id)})
    num_deleted = result.deleted_count
    print('delete() num_deleted:', num_deleted)
    flash('{} project(s) deleted'.format(num_deleted))
    return redirect(url_for('home.main'))


def get_project_views():
    projects = mongo.db.projects.find()
    # TODO: augment with owner, subscribers
    return projects
