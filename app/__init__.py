from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DB_USERNAME, DB_HOST, DB_NAME, DB_PASSWORD


app = Flask(__name__)
dbase = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dbase'

import models

dbase.create_all()
app.debug = True