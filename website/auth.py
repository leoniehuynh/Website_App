# Store organised routes for authentication applications using a Blueprint
# Import various modules
from flask import Blueprint

# Create and define Blueprint for auth variable
auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return "Login"

@auth.route("/sign-up")
def sign_up():
    return "Sign up"

@auth.route("/logout")
def logout():
    return "Logout"