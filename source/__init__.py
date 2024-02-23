from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()      #Database object
DB_NAME = "users.db"   #Database naam

def create_app():   #maakt een app aan
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bE<FNMOT`U--;F[=(>mL'   
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')   #registreert de views en auth blueprints
    app.register_blueprint(auth, url_prefix='/')    #url_prefix zorgt ervoor dat de url's van de blueprints worden aangepast

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager() #Login manager regelt de login en logout van de gebruikers
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):  #laad de user based op de user id
        return User.query.get(int(id))
    return app

def create_database(app): #maakt en database en database pad aan als deze nog niet bestaan
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)  
        print('Created Database!')