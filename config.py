import os
from dotenv import load_dotenv
from pathlib import Path

basedir = Path(__file__).parent
load_dotenv(basedir / '.env')

class Config(object):
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'random string'

    # Domain keys
    DOMAIN_CLIENT_ID = os.environ.get('DOMAIN_CLIENT_ID')
    DOMAIN_CLIENT_SECRET = os.environ.get('DOMAIN_CLIENT_SECRET')

    # Rental folder
    RENTAL_FOLDER = basedir / 'app/static/rental'

    # auto reload template without needing to restart Flask
    TEMPLATES_AUTO_RELOAD = True

    # Dev only so browser doesnt cache for CSS
    SEND_FILE_MAX_AGE_DEFAULT = 0
