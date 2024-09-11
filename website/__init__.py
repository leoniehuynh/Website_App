# Import various modules and functions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

# Create variable for and define name of database
db = SQLAlchemy()
DB_NAME = "database.db"

# Function to create and return Flask application
def create_app():
    app = Flask(__name__)
    # Configure Flask variables and Initialise database within Flask app
    app.config['SECRET_KEY'] = "t$cn:v}oWJE)-jC"
    app.config['SQL_ALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    # Import and Register Blueprints to Flask application
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    # Import User model
    from .models import User
    
    # Call create_database
    create_database(app)
    
    # Set up login manager and pass app
    login_manager=LoginManager
    # Redirect logged out users accessing restricted pages to login page
    login_manager.login_view = "auth.login"
    login.manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

# Function to check existence of, and create database 
def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        
        