import logging
import os

from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env_prod'
load_dotenv(dotenv_path=env_path)

from app.config_common import *


# DEBUG has to be to False in a production environment for security reasons
DEBUG = False

LOG_LEVEL = logging.INFO

ADMIN_CREDENTIALS = (
    os.environ.get('ADMIN_EMAIL'), os.environ.get('ADMIN_PASSWORD')
)
