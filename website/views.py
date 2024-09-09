# Store organised routes for core blog functions using a Blueprint
# Import Blueprint and various modules + functions
from flask import Blueprint, render_template

# Create and define Blueprint for views variable
views = Blueprint("views", __name__)

# Register core blog routes to views Blueprint that render templates
@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")