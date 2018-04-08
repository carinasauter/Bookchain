from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_material import Material

app = Flask(__name__, static_url_path='/static')
# Material(app)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app import views, models
