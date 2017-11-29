from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DB_USERNAME, DB_HOST, DB_NAME, DB_PASSWORD
import json

app = Flask(__name__)
dbase = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dbase'
app.config['SECRET_KEY'] = "Password"
import models


dbase.create_all()
app.debug = True

from app import controller