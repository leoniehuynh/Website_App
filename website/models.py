# Import db variable from __init__.py in current folder
# Import database, various modules and functions
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# =============== User Model ===============
'''
 Description
 Details
 Relationships
 
 - Primary key = id
 - Users are automatically given a unique id on successful signup
 
 Email has a maximum character length of 320, it must be unique to prevent duplicate emails
posts relationship reference all posts that the user has, any post with an author id = user id. 
addition on user table referencing users posts. backreference allows to access user model. 
passive delete allows all posts to be deleted when the user account is deleted.
'''

class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(150), unique=True)
   username = db.Column(db.String(150), unique=True)
   password = db.Column(db.String(150))
   date_created = db.Column(db.DateTime(timezone=True), default=func.now())
   posts = db.relationship('Post', backref='user', passive_deletes=True)
   likes = db.relationship('Like', backref='user', passive_deletes=True)
   comments = db.relationship('Comment', backref='user', passive_deletes=True)
    
# =============== Post Model ===============
'''
description appears on database table
give post unique id
require text and date_created
know author by referncing from user model id to know user
if user is deleted, the users posts are also deleted. through cascading on delete
nullable false means must have a value. one to many relationship where one user has many posts.
'''

class Post(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   text = db.Column(db.Text, nullable=False)
   date_created = db.Column(db.DateTime(timezone=True), default=func.now())
   author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
   likes = db.relationship('Like', backref='post', passive_deletes=True)
   comments = db.relationship('Comment', backref='post', passive_deletes=True)
    
# ================= Like Model =================
'''
description
'''

class Like(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   date_created = db.Column(db.DateTime(timezone=True), default=func.now())
   author = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"), nullable=False)
   post_id = db.Column(db.Integer, db.ForeignKey('post.id',ondelete="CASCADE"), nullable=False)
   
# =============== Comment Model ===============
'''
description
give comment unique id
require text and date_created
know author by referncing from user model id to know user
if user is deleted, the users posts are also deleted. through cascading on delete
nullable false means must have a value. one to many relationship where one user has many posts.
'''

class Comment(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   text = db.Column(db.Text, nullable=False)
   date_created = db.Column(db.DateTime(timezone=True), default=func.now())
   author = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"), nullable=False)
   post_id = db.Column(db.Integer, db.ForeignKey('post.id',ondelete="CASCADE"), nullable=False)