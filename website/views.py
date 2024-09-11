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
The Home function has access to all posts, this is so they can be displayed within the posts page.
Additionally, it will return the function, render_template, to redirect the user to the home.html
page.
'''

@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

# ============= Create Post Route and Function ============
'''
The Create Post function has been allowed the methods GET and POST so that it can pull from and
update the database of the flask application. It will create a post from user data and store
it into the database to be displayed. It is required that a user is logged into a user account 
to access the create post page.

It will request a text input from the user account through a form in order to create a post and 
commit it into the database so that it may be displayed in the home/posts page and a success
flash message appears and the user is redirected into the home / posts page. Otherwise, if the 
form has been submitted with no text, an error flash message appears and the create post template
page is rendered for the user to retry.
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
The User Posts function will search through the posts of the selected user through the
user account's username. It will check if the user account exists and if it does, then
the function will collect and display all posts made by the selected user account.

Otherwise, if the user account does not exist, then the function will flash an error
message and redirect the user back to the home page. It is required that a user is logged into a 
user account to access the create post page.
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
The Delete Post function will identify and delete an existing post from the database.
It will check the unique id given to the user post and check is the post exists. Then,
it will check if the user has the correct permissions to delete the post through the
post author id and the user account id of the user. If these prerequisites are met,
the post will be deleted from display and the database. It is required that a user 
is logged into a user account to access the create post page.

Otherwise, if the post does not exist or the user does not have sufficient permissions,
then the function will return an error flash message and return a redirect for the home
page.
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
