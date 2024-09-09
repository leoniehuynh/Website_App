# Store organised routes for core blog functions using a Blueprint
# Import Blueprint and various modules + functions
from flask import Blueprint, render_template

# Create and define Blueprint for views variable
views = Blueprint("views", __name__)

# Register routes to views Blueprint
# Define blog functions. Each will return the function, render_template, to render their respective HTML files from website/templates
@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")