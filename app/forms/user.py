from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Length, Email, EqualTo
from app.forms import Unique
from app.models import User


class Forgot(FlaskForm):

    ''' User forgot password form. '''

    email = TextField(
        validators=[Required(), Email()],
        description='Email address')


class Reset(FlaskForm):

    ''' User reset password form. '''

    password = PasswordField(
        validators=[
            Required(),
            Length(min=6),
            EqualTo('confirm', message='Passwords must match.')
        ],
        description='Password'
    )
    confirm = PasswordField(description='Confirm password')


class Login(FlaskForm):

    ''' User login form. '''

    email = TextField(
        validators=[Required(), Email()],
        description='Email'
    )
    password = PasswordField(
        validators=[Required()],
        description='Password'
    )


class SignUp(FlaskForm):

    ''' User sign up form. '''

    first_name = TextField(
        description='First Name',
        validators=[Required(), Length(min=2)],
    )
    last_name = TextField(description='Last Name')
    email = TextField(
        description='Email address',
        validators=[
            Required(),
            Email(),
            Unique(
                User,
                User.email,
                'This email address is already linked to an account.'
            )
        ],
    )
    password = PasswordField(
        description='Password',
        validators=[
            Required(),
            Length(min=6),
            EqualTo('confirm', message='Passwords must match.')
        ],
    )
    confirm = PasswordField(description='Confirm password')
