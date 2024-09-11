# Store organised routes for core blog functions using a Blueprint
# Import Blueprint, models, database, and various modules + functions
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db

# Create and define Blueprint for views variable
views = Blueprint("views", __name__)

# Register routes to views Blueprint

# =============== Home Route and Function ===============
''' 
Home function will return the function, render_template, to render their respective HTML files from website/templates
has access to the variable posts and can show them
'''

@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

# ============= Create Post Route and Function ============
'''
Allow methods
'''
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)

# ============ User Posts Route and Function =============
'''
Get all posts from chosen user
check if user exists and show all posts from user
'''

@views.route("/posts/<username>")
@login_required
def posts(username):
   user = User.query.filter_by(username=username).first()
   if not user:
       flash('No user with that username exists.', category='error;')
       return redirect(url_for('views.home'))
   
   posts = user.posts
   return render_template("posts.html", user=current_user, posts=posts, username=username)

# ============ Delete Post Route and Function =============
'''
description
check the id of post
check if correct person
and if so check if there is a post with id
then if permissions ok, delete post from database and refresh
'''

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
   post = Post.query.filter_by(id=id).first()
   if not post:
       flash("Post does not exist.", category='error')
   elif post.author != current_user.id:
       flash('You do not have permission to delete this post.', category='error')
   else:
       db.session.delete(post)
       db.session.commit()
       flash('Post deleted.', category='success')
   return redirect(url_for('views.home'))
