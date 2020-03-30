from pprint import pformat

from flask import (
    abort, Blueprint, flash, render_template, redirect, request, url_for, flash
)
from flask_login import current_user, login_required
from slugify import slugify
from sqlalchemy import inspect

from app import db
from app.forms.project import ProjectForm
from app.models import Project


projectbp = Blueprint('projectbp', __name__, url_prefix='/projects')


@projectbp.route('/submit/', methods=['GET', 'POST'])
@login_required
def submit():
    form = ProjectForm(formdata=request.form)
    was_submitted = request.method == 'POST'
    print('project.submit() was_submitted:', was_submitted)               ,
    if was_submitted:
        is_valid = form.validate()
        if is_valid:
            project_dict = {
                'title': form.title.data,
                'description': form.description.data,
                'needed': form.needed.data,
                'provided': form.provided.data,
                'contact': form.contact.data,
                'created_by_user_id': current_user.id,                                               'created_by_user': current_user,
                'users_joined': [current_user]
            }
            print('project.submit() project_dict:', project_dict)
            project = Project(**project_dict)
            db.session.add(project)
            db.session.commit()
            return redirect(url_for('projectbp.view', project_id=project.id))
        else:
            flash(
                'There was an error with your submission, please try again',
                'error'
            )

    return render_template(
        'project/submit.html',
        title='Submit a Project',
        action='submit',
        form=form,
        is_invalid=was_submitted and (not is_valid)
    )

@projectbp.route('/<project_id>/', methods=['GET', 'POST'])
@projectbp.route('/<project_id>/<user_slug>/', methods=['GET', 'POST'])
def view(project_id, user_slug=None):
    print('project_id:', project_id)
    print('user_slug:', user_slug)
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return abort(404)
    slug = slugify(project.title)
    if slug != user_slug:
        return redirect(url_for(
            'projectbp.view', project_id=project_id, user_slug=slug
        ))
    columns = [c for c in inspect(Project).columns]

    # XXX hack
    # TODO: figureout how to do this with wtforms_alchemy
    field_by_key = {
        column.key: {
            'label': column.info.get('label'),
            'data': getattr(project, column.key)
        }
        for column in inspect(Project).columns
        if not column.key.endswith('id')
        and not 'timestamp' in column.key
        and not 'title' in column.key
    }

    return render_template(
        'project/view.html',
        title=project.title,
        project=project,
        field_by_key=field_by_key
    )


@projectbp.route('/', methods=['GET', 'POST'])
def list():
    projects = Project.query.all()
    return render_template(
        'project/list.html', title='List Projects', projects=projects
    )

@projectbp.route('/join/<project_id>/', methods=['GET', 'POST'])
@login_required
def join(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        flash('No such project exists', 'error')
    else:
        if current_user in project.users_joined:
            # if user tried to join a project they were already a part of
            # while they were signed out, don't remove them
            if url_for('userbp.signin') in request.referrer:
                flash('You have already joined this project')
            else:
                project.users_joined.remove(current_user)
                flash('You have left the project')
        else:
            project.users_joined.append(current_user)
            flash('You have joined the project')
        db.session.commit()
    return redirect(url_for('projectbp.view', project_id=project.id))


@projectbp.route('/<project_id>/edit/', methods=['GET', 'POST'])
@projectbp.route('/<project_id>/<user_slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(project_id, user_slug=None):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        flash('No such project exists', 'error')
        return redirect(url_for('projectbp.list'))

    if not (
        current_user.is_superadmin or
        current_user.id == project.created_by_user_id
    ):
        flash('You don\'t have permission to do that')
        return redirect(url_for('projectbp.view', project_id=project_id))

    if request.method == 'GET':
        form = ProjectForm(obj=project)
        form.populate_obj(project)
    else:
        form = ProjectForm(formdata=request.form)

    # XXX HACK
    # read in project.forms.SubmitProjectForm.validate_title()
    form._project_id = int(project_id)

    was_submitted = request.method == 'POST'
    print(
        'project.edit() form:', form,
        'request.method:', request.method,
        'was_submitted:', was_submitted
    )
    if was_submitted:
        is_valid = form.validate()
        if is_valid:
            print('form:', pformat(vars(form)))
            project_dict = {
                'title': form.title.data,
                'description': form.description.data,
                'needed': form.needed.data,
                'provided': form.provided.data,
                'contact': form.contact.data,
                'budget': form.budget.data,
                'decision_making': form.decision_making.data
            }
            print('project.submit() project_dict:', project_dict)
            for key, val in project_dict.items():
                setattr(project, key, val)
            db.session.commit()
            return redirect(url_for(
                'projectbp.view',
                project_id=project_id,
                user_slug=slugify(project.title)
            ))
        else:
            flash(
                'There was an error with your submission, please try again',
                'error'
            )
    else:
        is_valid = True
    submission_is_invalid = (not is_valid) and was_submitted
    return render_template(
        'project/submit.html',
        title='Edit',
        action='edit',
        form=form,
        project=project,
        is_invalid=submission_is_invalid
    )


@projectbp.route('/delete/<project_id>/', methods=['POST'])
def delete(project_id):
    project = db.session.query(Project).filter(Project.id==project_id).first()
    print('project.delete() project:', project)
    db.session.delete(project)
    db.session.commit()
    flash('Project was deleted')
    return redirect(url_for('projectbp.list'))
