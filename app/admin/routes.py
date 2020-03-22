import os
import random
import string

from flask import abort, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from app import bcrypt, mongo
from app.admin import admin_blueprint
from app.admin.forms import InviteForm


def get_invite_code(size=5):
    invite_code = ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=size
        )
    )
    print('get_invite_code() invite_code:', invite_code)
    return invite_code


# TODO: move to manage.py
@admin_blueprint.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():
    user = mongo.db.projects.find_one({'can_invite_users': 'true'})
    print('admin.bootstrap() existing user:', user)
    if not user:
        user = mongo.db.users.insert({
            'email': os.environ['ADMIN_EMAIL'],
            'name': 'Admin',
            'password': bcrypt.generate_password_hash(
                os.environ['ADMIN_PASSWORD']
            ),
            'authenticated': False,
            'can_invite_users': True
        })
        print('admin.bootstrap() inserted user:', user)
    return redirect(url_for('user.login'))


@admin_blueprint.route('/invite', methods=['GET', 'POST'])
@login_required
def invite():
    if not current_user.can_invite_users:
        abort(404)
    invite_url = None
    invites = mongo.db.invites.find()
    if request.method == 'POST':
        invite_code = get_invite_code()
        host = request.host
        invite_url = url_for('user.register', invite_code=invite_code)
        invite_url = '{}{}'.format(host, invite_url)
        invite = mongo.db.invites.insert({
            'user_id': None,
            'invite_code': invite_code
        })
        print('admin.invite() new invite:', invite)
    return render_template('admin/invite.html', invite_url=invite_url)
