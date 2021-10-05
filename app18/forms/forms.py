# Copyright 2021 Franklin Siqueira.
# SPDX-License-Identifier: Apache-2.0

"""
Create forms logic
"""
from wtforms import Form, StringField, PasswordField, validators, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional, InputRequired


class SignupForm(Form):
    """
    User Signup Form
    """

    name = StringField('Name',
                       validators = [DataRequired(message=("Enter a user name, please."))])
    
    email = StringField('Email',
                        validators = [Length(min=6, message=("Please, enter a valid email address.")), 
                                    Email(message=("Please, enter a valid email address.")), 
                                    DataRequired(message=("Please, enter a valid email address."))])
    
    password = PasswordField('Password',
                             validators=[DataRequired(message = "A password is required!"),
                                         Length(min = 6, message =("Please, select a stronger password.")),
                                         EqualTo('confirm', message = "Passwords must match")])
    
    confirm = PasswordField("Confirm your password",)
    
    website = StringField('Website',
                          validators=[Optional()])
    
    submit = SubmitField("Register!")


class LoginForm1(Form):
    """
    User Login1 Form
    """

    email = StringField('Email', 
                        validators = [DataRequired("Please, enter a valid email address."), 
                                      Email("Please, enter a valid email address.")])
    
    password = PasswordField('Password', 
                             validators = [DataRequired("A password is required!")])
    
    submit = SubmitField("Log In")

# from app18
class LoginForm(Form):
    """
    User Login Form
    """
    username = StringField('username', 
                           validators = [DataRequired(message=("Enter an user name, please."))])
    password = PasswordField('password', 
                             validators = [DataRequired("A password is required!")])
    remember = BooleanField('remember me')
    
    submit = SubmitField('Log In')

class RegisterForm(Form):
    """
    Register User Form
    """
    email = StringField('email', 
                        validators = [DataRequired("Please, enter a valid email address."), 
                                      Email("Please, enter a valid email address.")])
    username = StringField('username', 
                           validators = [DataRequired(message=("Enter an user name, please."))])
    password = PasswordField('password', 
                             validators = [DataRequired("A password is required!")])
    
    submit = SubmitField('Signup')
#####################      End      ########################