# Import db variable from __init__.py in current folder
# Import various modules and functions
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

'''
 The User Database Model:
 - Primary key = id
 - Users are automatically given a unique id on successful signup
 
 Email has a maximum character length of 320, it must be unique to prevent duplicate emails
 
'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
    
    
    