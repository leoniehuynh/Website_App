# Store organised routes for authentication functions using a Blueprint
# Import Blueprint and various modules + functions
from flask import Blueprint, render_template, redirect, url_for, request


# Create and define Blueprint for auth variable
auth = Blueprint("auth", __name__)


# Register routes to auth Blueprint, allow for GET and POST requests
# Define login function, receives data from login form and returns render_template for login.html
@auth.route("/login", methods=['GET', 'POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    
    return render_template("login.html")

# Define sign_up function, receives data from signup form and returns render_template for signup.html
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    email = request.form.get("email")
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password")
    
    return render_template("signup.html")


# Define logout function, returns a redirect to url_for the home function in views.py
@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))