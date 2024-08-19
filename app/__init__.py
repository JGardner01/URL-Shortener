from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

load_dotenv() #google api key

#initialise app
app = Flask(__name__, template_folder="templates")

#connect and set up mongo db
client = MongoClient("localhost", 27017)
db = client.url_shortener
urls = db.urls
users = db.users

#for hashing passwords
bcrypt = Bcrypt(app)

from app import routes