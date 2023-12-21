# website/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = "Danush@#1405"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from.models import models

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(models, url_prefix='/')

    # Create tables if they do not exist
    with app.app_context():
        db.create_all()

    return app




