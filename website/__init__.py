# Import various modules and functions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

# Create and return Flask application
def create_app():
    app = Flask(__name__)
    # Configure Flask variables
    app.config['SECRET_KEY'] = "t$cn:v}oWJE)-jC"
    
    # Import and Register Blueprints to Flask application
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    return app