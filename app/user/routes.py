from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import mongo, bcrypt, login_manager
from app.user import user_blueprint, User


@login_manager.user_loader
def load_user(email):
    users = mongo.db.users.find_one({'email': email})
    if not users:
        return None
    return User(users['email'], users['name'])


@user_blueprint.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('home.main'))


@user_blueprint.route('/login', methods=['POST', 'GET'])
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
        user = mongo.db.users.find_one({'email': email})
        if user:
            if User.validate_login(user['password'], password):
                user_obj = User(email, user['name'])
                login_user(user_obj)
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


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
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
            return render_template('user/register.html')
        else:
            user = mongo.db.users.insert({
                'email': email,
                'name': name,
                'password': bcrypt.generate_password_hash(password),
                'authenticated': False
            })
            print('register() new user:', user)
            msg = 'Logged in successfully.'
            print('register() msg', msg)
            flash(msg, 'info')
            user_obj = User(email, name)
            login_user(user_obj)
            return redirect(url_for('home.main'))
    else:
        return render_template('user/register.html')
