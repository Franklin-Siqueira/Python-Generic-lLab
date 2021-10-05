# Copyright 2021 Franklin Siqueira.
# SPDX-License-Identifier: Apache-2.0

'''
Created on Jul 13, 2019

@author: Franklin Siqueira

References:

1) 

2) 
'''
from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()

login_manager = LoginManager()

def create_app():
    """
    Build the core application
    """
    
    app = Flask(__name__, instance_relative_config = True)

    # Application Configuration
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
#     app.config['SECRET_KEY'] = "Thisissupposedtobesecret!" #.from_object('config.DevelopmentConfig') # was (config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://jovbxjjwysiory:5185debfdb0b3abab22d9ebfa2d555801a6844511e276ec80bd9228c402fbc91@ec2-50-19-222-129.compute-1.amazonaws.com:5432/db26onrhlbj9pt?sslmode=require"
    # Local: "postgresql://postgres:245353f10I@localhost/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config.from_object("config")
#     app.config.from_pyfile("config.py")
# From Google OAuth client ID = 161904758826-5jdplndeidus95s3f0epdand7kae4pta.apps.googleusercontent.com
# secret = 5ZYDZIZPZqS3ejWt-EnLbfTz
#     GOOGLE_CLIENT_ID = "161904758826-5jdplndeidus95s3f0epdand7kae4pta.apps.googleusercontent.com" #os.environ.get("GOOGLE_CLIENT_ID", None)
#     GOOGLE_CLIENT_SECRET = "5ZYDZIZPZqS3ejWt-EnLbfTz" # os.environ.get("GOOGLE_CLIENT_SECRET", None)
#     GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    
    from .models.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # Import parts of our application
        from .models import main
        from .models import auth
        from .models import analysis
        from .models import products
        app.register_blueprint(main.mainBP)
        app.register_blueprint(auth.authBP)
        app.register_blueprint(analysis.analysisBP)
        app.register_blueprint(products.productsBP)
        print(app.secret_key)

        # Create Database Models
        db.create_all()

    return app