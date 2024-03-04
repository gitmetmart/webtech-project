from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()      # Database object
DB_NAME = "users.db"   # Database name

def create_app():
    """
    Maakt en configureert de Flask-toepassing.

    Returns:
        app (Flask): Het Flask-toepassingsobject.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bE<FNMOT`U--;F[=(>mL'   
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        """
        Laadt een gebruiker op basis van de gebruikers-id.

        Args:
            id (int): De gebruikers-id.

        Returns:
            User: Het User-object.
        """
        return User.query.get(int(id))
    return app

def create_database(app):
    """
    Maakt de database en het databasepad aan als ze niet bestaan.

    Args:
        app (Flask): Het Flask-toepassingsobject.
    """
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)  
        print('Database aangemaakt!')
