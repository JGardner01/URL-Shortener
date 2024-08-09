from flask import Flask
from pymongo import MongoClient
app = Flask(__name__, template_folder="templates")

client = MongoClient("localhost", 27017)
db = client.url_shortener
urls = db.urls


from app import routes

