# Store organised routes for core blog applications using a Blueprint
# Import various modules
from flask import Blueprint

# Create and define Blueprint for views variable
views = Blueprint("views", __name__)

@views.route("/")
def home():
    return "Home"