import os
import pymongo

basedir = os.path.abspath(os.path.dirname(__file__))

class Config: 
    # creates some secret key so that flaskwtf forms will work. 
    SECRET_KEY = ''
    # Creates some connection to the MongoDB database. 
    mongo_connection = ''
    
