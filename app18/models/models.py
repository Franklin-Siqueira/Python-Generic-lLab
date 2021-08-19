"""
Database models
"""
from flask_sqlalchemy  import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

###################################################################
#                       Database Class 
###################################################################

db = SQLAlchemy()
SQLALCHEMY_TRACK_MODIFICATIONS = False

class Data(db.Model):
    '''data table model for the heights routine'''
    
    __tablename__= "data"
    
    id = db.Column(db.Integer, 
                   primary_key = True)
    
    email = db.Column(db.String(120), 
                      unique = True)
    
    height = db.Column(db.Integer)
    
    country = db.Column(db.String(120), 
                      unique = True)

    def __init__(self, email_, height_, country_):
        self.email = email_
        self.height = height_
        self.country = country_

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(200))
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

# class User(UserMixin, db.Model):
#     """Model for user accounts"""
# 
#     __tablename__ = 'flasklogin-users'
# 
#     id = db.Column(db.Integer,
#                    primary_key = True)
#     
#     name = db.Column(db.String,
#                      nullable = False,
#                      unique = False)
#     
#     email = db.Column(db.String(40),
#                       unique = True,
#                       nullable = False)
#     
#     password = db.Column(db.String(200),
#                          primary_key = False,
#                          unique = False,
#                          nullable = False)
#     
#     website = db.Column(db.String(60),
#                         index = False,
#                         unique = False,
#                         nullable = True)
#     
#     created_on = db.Column(db.DateTime,
#                            index = False,
#                            unique = False,
#                            nullable = True)
#     
#     last_login = db.Column(db.DateTime,
#                            index = False,
#                            unique = False,
#                            nullable = True)
# 
#     def set_password(self, password):
#         """Create hashed password"""
#         
#         self.password = generate_password_hash(password, method = 'sha256')
# 
#     def check_password(self, password):
#         """Check hashed password"""
#         
#         return check_password_hash(self.password, password)
# 
#     def __repr__(self):
#         return '<User {}>'.format(self.username)
