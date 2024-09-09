# Store organised routes for authentication functions using a Blueprint
# Import Blueprint and various modules + functions
from flask import Blueprint, render_template, redirect, url_for

# Create and define Blueprint for auth variable
auth = Blueprint("auth", __name__)

# Register routes to auth Blueprint
# Define authentication functions. Each will return the function, render_template, to render their respective HTML files from website/templates
@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/sign-up")
def sign_up():
    return render_template("signup.html")

# The function, logout, will return a redirect to the url for the home function in the views Blueprint
@auth.route("/logout")
def logout():
    return redirect(url_for("views.home"))