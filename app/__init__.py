from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
dbase = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dbase'
app.config['SECRET_KEY'] = "Password"
import models
Bootstrap(app)

dbase.create_all()
app.debug = True

from app import controller