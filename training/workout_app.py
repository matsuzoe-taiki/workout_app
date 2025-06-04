from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
from sqlalchemy import Float
from datetime import datetime


db_uri = 'mysql+pymysql://root:@localhost:3306/workout_db?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


