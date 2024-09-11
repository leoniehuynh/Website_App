# Store organised routes for authentication functions using a Blueprint
# Import Blueprint and various modules + functions
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import user

# Create and define Blueprint for auth variable
auth = Blueprint("auth", __name__)


# Register routes to auth Blueprint, allow for GET and POST requests
# Define login function, receives data from login form and returns render_template for login.html

# ========== Login Route ==========
@auth.route("/login", methods=['GET', 'POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    
    return render_template("login.html")

# ========== Sign Up Route ==========
# Define sign_up function, receives data from signup form and returns render_template for signup.html
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    # Retrieve POST data
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password")
        
        # Create User Account, Add to database, and Redirect to home.html if prerequisites are met
        # Create variables to check if email and username exist in database
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password2 != password1:
            flash('Passwords do not match.', category='error')
        elif len(username) < 6:
            flash('Username is too short. Username must be between 6-30 characters.', category='error')
        elif len(username) > 30:
            flash('Username is too long. Username must be between 6-30 characters.', category='error')
        elif len(password1) < 8:
            flash('Password is too short. Password must be longer than 7 characters.', category='error')
        elif len(email) < 3:
            flash('Invalid email.', category='error')
        else: # Additionally generate password hash using sha256 encryption
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method=sha256))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!')
            return redirect(url_for(views.home))
    
    # Return signup.html if prerequisites are not met
    return render_template("signup.html")

# ========== Logout Route ==========
# Define logout function, returns a redirect to url_for the home function in views.py
@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))