# Store organised routes for core blog functions using a Blueprint
# Import Blueprint and various modules + functions
from flask import Blueprint, render_template
from flask_login import login_required, current_user

# Create and define Blueprint for views variable
views = Blueprint("views", __name__)

# Register routes to views Blueprint
# Home function will return the function, render_template, to render their respective HTML files from website/templates
@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", name=current_user.username)