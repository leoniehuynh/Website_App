# Import various modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

# Create and return Flask application
def create_app():
    app = Flask(__name__)
    # Configure Flask variables
    app.config['SECRET_KEY'] = "t$cn:v}oWJE)-jC"
    
    return app