from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config

app = Flask(__name__)

db = SQLAlchemy(app)
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(Config)
from app import views