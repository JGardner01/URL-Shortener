from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.auth.models import User
import os

def create_app():
    load_dotenv()  #load environment variables (google api key and secret key)

    #initialise flask app
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.getenv("SECRET_KEY")

    #connect to mongo db
    client = MongoClient("localhost", 27017)
    db = client.url_shortener
    app.db = db
    app.urls = db.urls
    app.users = db.users

    #initialise bcrypt for hashing passwords
    bcrypt = Bcrypt(app)
    app.bcrypt = bcrypt

    #initialise login manager
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"  #redirect

    @login_manager.user_loader
    def load_user(username):
        user_data = app.users.find_one({"username": username})

        if user_data:
            return User(username=user_data["username"])
        return None


    #import and register blueprints
    from app.main import main as main_blueprint
    from app.auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app

