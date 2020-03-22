import os

from dotenv import load_dotenv


load_dotenv(verbose=True)

MONGO_DBNAME = 'oc19'
MONGO_URI = os.environ['MONGO_URI']
