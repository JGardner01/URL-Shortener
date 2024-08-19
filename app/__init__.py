from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .models import User

load_dotenv() #google api key

#initialise app
app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY")

#connect and set up mongo db
client = MongoClient("localhost", 27017)
db = client.url_shortener
urls = db.urls
users = db.users

#initialise login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  #redirect

#for hashing passwords
bcrypt = Bcrypt(app)

from app import routes


@login_manager.user_loader
def load_user(username):
    user_data = users.find_one({"username": username})

    if user_data:
        return User(username=user_data["username"])
    return None
