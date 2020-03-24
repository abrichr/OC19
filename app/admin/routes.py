import os
import random
import string

from flask import abort, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from app import bcrypt, mongo
from app.bootstrap import maybe_do_bootstrap
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
    maybe_do_bootstrap()
    return redirect(url_for('home.main'))


def get_invite_views():
    invite_views = []
    invites = mongo.db.invites.find()
    invites = [invite for invite in invites]
    user_ids = [invite['user_id'] for invite in invites if invite['user_id']]
    print('get_invite_views() user_ids:', user_ids)
    users = mongo.db.users.find({
        '_id': {
            '$in': user_ids
        }
    })
    users = [user for user in users]
    print('get_invite_views() users:', users, 'invites:', invites)
    email_by_id = {user['_id']: user['email'] for user in users}
    for invite in invites:
        user_id = invite['user_id']
        email = email_by_id.get(user_id)
        invite_code = invite['invite_code']
        invite_link, invite_href = get_invite_link(invite_code)
        invite_views.append({
            'invite_link': invite_link,
            'invite_href': invite_href,
            'email': email
        })
    print('get_invite_views() invite_views:', invite_views)
    return invite_views


def get_invite_link(invite_code):
    host = request.host
    invite_href = url_for('user.register', invite_code=invite_code)
    invite_link = '{}{}'.format(host, invite_href)
    print(
        'get_invite_link() invite_code:', invite_code,
        'invite_href:', invite_href,
        'invite_link:', invite_link
    )
    return invite_link, invite_href


@admin_blueprint.route('/invite', methods=['GET', 'POST'])
@login_required
def invite():
    if not current_user.can_invite_users:
        abort(404)
    invite_link = None
    if request.method == 'POST':
        invite_code = get_invite_code()
        invite_link, invite_href = get_invite_link(invite_code)
        invite = mongo.db.invites.insert({
            'user_id': None,
            'invite_code': invite_code
        })
        print('admin.invite() new invite:', invite)
    invite_views = get_invite_views()
    return render_template(
        'admin/invite.html',
        invite_link=invite_link,
        invite_views=invite_views
    )
