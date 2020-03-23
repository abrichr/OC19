from bson.objectid import ObjectId
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from app import mongo, bcrypt
from app.user import user_blueprint, User, load_user


@user_blueprint.route('/profile/')
@login_required
def profile():
    return render_template('user/profile.html')


@user_blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('home.main'))


@user_blueprint.route('/login/', methods=['POST', 'GET'])
def login():

    def invalid_credentials():
        #TODO: use logging
        msg = 'Invalid credentials'
        print('login() msg:', msg)
        flash(msg, 'error')
        render_template('user/login.html')

    if request.method == 'POST':
        email = request.form['input-email']
        password = request.form['input-password']
        user = load_user(email)
        print('user.login() user:', user)
        if user:
            if User.validate_login(user.password_hash, password):
                login_user(user)
                msg = 'Logged in successfully.'
                print('login() msg', msg)
                flash(msg, 'info')
                next_url = request.args.get('next', url_for('home.main'))
                return redirect(next_url)
            else:
                invalid_credentials()
        else:
            invalid_credentials()
    return render_template('user/login.html')


def set_invite_user(invite, user_id):
    if not invite:
        return
    invite_id = invite['_id']
    print('admin.set_invite_user() invite_id:', invite_id, 'user_id:', user_id)
    result = mongo.db.invites.update_one({
        '_id': ObjectId(invite_id)
    }, {
        '$set': {
            'user_id': user_id
        }
    })
    modified_count = result.modified_count
    print('set_invite_user() invite modified_count:', modified_count)


@user_blueprint.route('/register/', methods=['GET', 'POST'])
@user_blueprint.route('/register/<invite_code>/', methods=['GET', 'POST'])
def register(invite_code=None):
    invite = mongo.db.invites.find_one({'invite_code': invite_code})
    if invite_code and ((not invite) or invite['user_id']):
        print('user.register() invalid invite_code:', invite_code)
        flash('Invalid invite code', 'error')
        return redirect(url_for('user.register'))
    if request.method == 'POST':
        name = request.form['input-name']
        email = request.form['input-email']
        password = request.form['input-password']
        print('register() name:', name, 'email:', email, 'password:', password)
        user = mongo.db.users.find_one({'email': email})
        print('register() existing user:', user)
        if user:
            msg = 'User already exists'
            print('register() msg:', msg)
            flash(msg, 'error')
            return render_template(
                'user/register.html', invite_code=invite_code
            )
        else:
            user_dict = {
                'email': email,
                'name': name,
                'password': bcrypt.generate_password_hash(password),
                'authenticated': False,
                'can_invite_users': False,
                'can_create_projects': bool(invite_code)
            }
            result = mongo.db.users.insert_one(user_dict)
            user_id = result.inserted_id
            print('register() new user_dict:', user_dict, 'user_id:', user_id)
            set_invite_user(invite, user_id)
            msg = 'Logged in successfully.'
            print('register() msg', msg)
            flash(msg, 'info')
            user = load_user(email, user_dict)
            login_user(user)
            return redirect(url_for('home.main'))
    else:
        return render_template('user/register.html', invite_code=invite_code)


@user_blueprint.route('/view/<user_id>/', methods=['GET'])
def view(user_id):
    print('user.view() user_id:', user_id)
    user = mongo.db.users.find_one({'_id': ObjectId(user_id) })
    print('user.view() user:', user)
    projects = mongo.db.projects.find({'user_id': ObjectId(user_id)})
    return render_template('user/view.html', user=user, projects=projects)
