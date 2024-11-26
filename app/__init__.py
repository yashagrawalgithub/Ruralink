from flask import Flask
from config import Config
from flask_pymongo import PyMongo
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MySQL
mysql = MySQL(app)

# Initialize MongoDB
mongo = PyMongo(app)

# Import routes
from app import routes
