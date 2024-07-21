from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager



db = SQLAlchemy()
DB_NAME = "database.db"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'KEY2'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    db.init_app(app)
    
    from .auth import auth
    from .routes import routes

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')
    
    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    return app
  

