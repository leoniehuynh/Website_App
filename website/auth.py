# Store organised routes for authentication functions using a Blueprint
# Import Blueprint and various modules + functions
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

# Create and define Blueprint for auth variable
auth = Blueprint("auth", __name__)


# Register routes to auth Blueprint, allow for GET and POST requests
# Define login function, receives data from login form and returns render_template for login.html

# =============== Login Route and Function ===============
'''
Purpose of route and stuff
'''
# ========================================================

@auth.route("/login", methods=['GET', 'POST'])
def login():
    # Retrieve POST data
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if user exists in database and if user password is correct, Login user within session and Redirect to home.html if so
    user = User.query.filter_by(email=email).first()
    if user: # if user exists and password is correct
        if check_password_hash(user.password, password):
            flash("Logged in successfully!", category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else: # if password is incorrect
            flash('Incorrect password', category='error')
    else: # if user does not exist
        flash('No user account with this email exists.', category='error')

    return render_template("login.html")
        
# =============== Signup Route and Function ===============
'''
Define sign_up function, receives data from signup form and returns render_template for signup.html
'''
# =========================================================

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    # Retrieve POST data
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        # Create user account, Add to database, Login user, and Redirect to home.html if prerequisites are met
        # Create variables to check if email and username exist in database
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(username) < 6 or len(username) > 30:
            flash('Username must be between 6-30 characters.', category='error')
        elif len(password1) < 8:
            flash('Password is too short. Password must be longer than 7 characters.', category='error')
        elif len(email) < 3:
            flash('Invalid email.', category='error')
        else: # Additionally generate password hash for password
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!')
            return redirect(url_for('views.home'))
    
    # Return signup.html template if prerequisites are not met
    return render_template("signup.html")

# =============== Logout Route and Function ===============
''' 
Define logout function, returns a redirect to url_for the home function in views.py
'''
# =========================================================
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", category=('success'))
    return redirect(url_for("views.home"))

