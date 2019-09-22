from flask import Flask
from config import Config
from authlib.client import OAuth2Session


app = Flask(__name__)
app.config.from_object(Config)

# oauth2 domain
scope='api_listings_read'
domain = OAuth2Session(app.config['DOMAIN_CLIENT_ID'], app.config['DOMAIN_CLIENT_SECRET'], scope=scope)
token = domain.fetch_access_token('https://auth.domain.com.au/v1/connect/token', grant_type='client_credentials')

from app.main import bp as main_bp
app.register_blueprint(main_bp)
