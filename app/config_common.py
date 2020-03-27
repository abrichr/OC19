import os

DEBUG = False

TIMEZONE = 'America/Toronto'

# Secret key for generating tokens
SECRET_KEY = 'houdini'

# Admin credentials
ADMIN_CREDENTIALS = (
    os.environ.get('ADMIN_EMAIL'), os.environ.get('ADMIN_PASSWORD')
)

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'pa$$word')

# Database choice
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuration of a Gmail account for sending mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'oncovid19team@gmail.com'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
ADMINS = ['oncovid19team@gmail.com']

# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12

LOG_FILENAME = 'activity.log'
LOG_MAXBYTES = 1024
LOG_BACKUPS = 2

TOASTR_POSITION_CLASS = 'toast-top-center'
