from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

from app.main import bp as main_bp
app.register_blueprint(main_bp)
