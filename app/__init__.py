from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.auth.models import User
from app.main.urls_cleanup import start_scheduler

def create_app(config):
    #initialise flask app
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config)


    #connect to mongo db
    client = MongoClient(app.config["MONGO_URI"])
    db = client.get_default_database()
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

    start_scheduler(app)

    return app

