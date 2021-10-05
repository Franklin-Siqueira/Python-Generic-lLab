# Copyright 2021 Franklin Siqueira.
# SPDX-License-Identifier: Apache-2.0

'''
Created on Jul 13, 2019

@author: franklincarrilho
'''
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# custom
from app18.models.models import User
from app18 import db
from app18.forms.forms import LoginForm, RegisterForm

authBP = Blueprint("auth", __name__, 
                 template_folder = "templates",
                 static_folder = "static")

###################################################################
#                          routes                                 #
###################################################################
#
#
#                        login Route 
#
#
###################################################################
@authBP.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Description:
    
    '''
    form = LoginForm()

    if form.validate_on_submit():
        
        user = User.query.filter_by(username = form.username.data).first()
        
        if user:
            
            if check_password_hash(user.password, form.password.data):
                
                login_user(user, remember = form.remember.data)
                
                return redirect(url_for("main.home"))

        flash("Incorrect user or password!")
        return redirect(url_for("auth.login"))
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template("login.html", form = form)
###################################################################
#
#
#                        signup Route 
#
#
###################################################################
@authBP.route("/signup", methods=["GET", "POST"])
def signup():
    '''
    Description:
    
    '''    
    form = RegisterForm()

    if form.validate_on_submit():
        
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        
        if user:
            flash("Informed e-mail already registered!")
            return redirect(url_for("auth.login"))
            
        # generate hash password
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # instantiate new user
        new_user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        # insert new user
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("main.home"))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form = form)
###################################################################
#
#
#                           logout route 
#
#
###################################################################
@authBP.route('/logout')
@login_required
def logout():
    '''
    Description:
    
    '''   
    logout_user()
    
    return redirect(url_for("main.home"))
