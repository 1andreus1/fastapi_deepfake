import os

from dotenv import load_dotenv

load_dotenv()

# REDIS_URL = 'redis://default:redispw@localhost:49153'
# QUEUE_NAME = 'tasks'
#
# DOWNLOADS_DIR = '../downloads/'
# UPLOADS_DIR = '../uploads/'


DOWNLOADS_DIR = os.environ.get("DOWNLOADS_DIR")
UPLOADS_DIR = os.environ.get("UPLOADS_DIR")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
QUEUE_NAME = os.environ.get("QUEUE_NAME")
