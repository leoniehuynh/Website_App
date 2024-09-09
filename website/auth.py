# Store organised routes for authentication functions using a Blueprint
# Import Blueprint and various modules + functions
from flask import Blueprint, render_template

# Create and define Blueprint for auth variable
auth = Blueprint("auth", __name__)

# Register authentication routes to auth Blueprint that render templates
@auth.route("/login")
def login():
    return "Login"

@auth.route("/sign-up")
def sign_up():
    return "Sign up"

@auth.route("/logout")
def logout():
    return "Logout"