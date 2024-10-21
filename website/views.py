# Store organised routes for core blog functions using a Blueprint
# Import Blueprint, models, database, and various modules + functions
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db

# Create and define Blueprint for views variable
views = Blueprint("views", __name__)

# Register routes to views Blueprint

# =============== Home & Blog Route and Function ===============
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

@views.route("/blog")
@login_required
def blog():
   posts = Post.query.all()
   return render_template("posts_div.html", user=current_user, posts=posts)

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
            return redirect(url_for('views.blog'))

    return render_template('create_post.html', user=current_user)

# ============ Like Posts Route and Function =============
'''
The User Likes function has been allowed the POST method. The purpose of the function is to check
whether a post exists and if it does, it will check if the user has liked the post. If the user
has not liked the post, then it will like the post. If the user has liked the post, it will unlike
the post. It is required that a user is logged into a user account to access. Javascript calls for this.
'''
@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

# ============ User Posts Route and Function =============
'''
The User Posts function will search through the posts of the selected user through the
user account's username. It will check if the user account exists and if it does, then
the function will collect and display all posts made by the selected user account.

Otherwise, if the user account does not exist, then the function will flash an error
message and redirect the user back to the posts page. It is required that a user is logged into a 
user account to access the user posts page.
'''

@views.route("/posts/<username>")
@login_required
def posts(username):
   user = User.query.filter_by(username=username).first()
   if not user:
       flash('No user with that username exists.', category='error')
       return redirect(url_for('views.blog'))
   
   posts = user.posts
   return render_template("posts.html", user=current_user, posts=posts, username=username)

# ============ Delete Post Route and Function =============
'''
The Delete Post function will identify and delete an existing post from the database.
It will check the unique id given to the user post and check is the post exists. Then,
it will check if the user has the correct permissions to delete the post through the
post author id and the user account id of the user. If these prerequisites are met,
the post will be deleted from display and the database. It is required that a user 
is logged into a user account to access the delete post page.

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
   return redirect(url_for('views.blog'))

# ============ Create Comment Route and Function =============
'''
The Create Comment function is allowed for the POST method, it displays a form to the 
user account that, once filled in, will create a comment, store it into the database,
and have it displayed under the post it was commented on. The user must be authenticated
to comment under a post.

Otherwise, if the prerequisites are not met, then the function will flash an error 
message then redirect to the home page.
'''

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
   text = request.form.get('text')
   if not text:
       flash('Comment cannot be empty.', category='error')
   else:
       post = Post.query.filter_by(id=post_id)
       if post:
           comment = Comment(text=text, author=current_user.id, post_id=post_id)
           db.session.add(comment)
           db.session.commit()
       else:
           flash('Post does not exist.', category='error')
   return redirect(url_for('views.blog'))

# ============ Delete Comment Route and Function =============
'''
The Delete Comment function checks if comment exists, if it does not, return an error. 
If it does, check if the current user has the permissions to delete the comment. If 
they do not, return an error flash message. If the user meets these two prerequisites,
the comment will be deleted from display and the database.
'''

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
       flash('Comment does not exist.', category='error')    
    elif current_user.id != comment.author and current_user.id != comment.post.author:
       flash('You do not have permission to delete this comment.', category='error')
    else:
       db.session.delete(comment)
       db.session.commit()
       
    return redirect(url_for('views.blog'))
       