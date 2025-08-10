from flask import Flask
from config import Config
from flask_pymongo import PyMongo
#from pymongo import MongoClient
#from pymongo.server_api import ServerApi

app = Flask(__name__)
app.config.from_object(Config)

uri = Config.mongo_connection
app.config["MONGO_URI"] = uri
mongo_connection = PyMongo(app)
mydb = mongo_connection.db

from app import routes