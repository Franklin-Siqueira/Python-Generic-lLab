# Copyright 2021 Franklin Siqueira.
# SPDX-License-Identifier: Apache-2.0

'''
Created on Jul 13, 2019

@author: franklincarrilho
'''
from os import environ


class Config:
    """
    Set Flask configuration variabless from .env file
    """

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # Static Assets
    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

class ProductionConfig(Config):
    """
    Set Flask configuration for production
    """
    
    SQLALCHEMY_DATABASE_URI = "postgres://cbiwrbhjnodoiw:949f872a8733788a368cf1442d768d2fc90e0e0de7c710a7797234cec7400589@ec2-174-129-227-80.compute-1.amazonaws.com:5432/d12bnhr3f6qla1?sslmode=require"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """
    Set Flask configuration for development
    """
    
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:245353f10I@localhost/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
#########################                  END            ###########################