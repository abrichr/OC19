import logging
import os

from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env_dev'
load_dotenv(dotenv_path=env_path)

from app.config_common import *


# DEBUG can only be set to True in a development environment for security reasons
DEBUG = True

# Secret key for generating tokens
SECRET_KEY = 'houdini'

# Admin credentials
ADMIN_CREDENTIALS = ('admin', 'admin')

LOG_LEVEL = logging.DEBUG

ADMIN_CREDENTIALS = (
    os.environ.get('ADMIN_EMAIL'), os.environ.get('ADMIN_PASSWORD')
)
