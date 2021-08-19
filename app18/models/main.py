'''
Created on Jul 13, 2019

@author: franklincarrilho
'''
from flask import Blueprint, render_template, request
import os
import sys
import requests
from pathlib import Path
import pandas as pd
from sqlalchemy.sql import func
from flask import Blueprint, render_template, request
# custom
from app18.stocks import getSP500Stocks, getB3Stocks, getDataB3Stocks, getDataSP500Stocks, condenseData
from app18.runtimeUtils import send_email
from app18.models.models import Data

mainBP = Blueprint("main", __name__, 
                 template_folder = "templates",
                 static_folder = "static")

###################################################################
#                          routes                                 #
###################################################################
#
#                                                        Home Route 
###################################################################
@mainBP.route('/', methods = ["POST", "GET"])
def home():
    # Modal variables
    messageHead = "Welcome to my Full Stack Test App!"
    messageBody = "I hope you have a good time here. Please, take some time to leave your opinion about the features offered here. I'd really appreciate that!"
    # read requirements.txt and pass to home
    requirementsText = []
    with open("requirements.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            requirementsText.append(line.rstrip("\n"))
            
    print(len(lines))   
    print(requirementsText)
    #
    ROOT_DIR4 = Path(__file__).parent.parent # /app18_Admin2/app18/
    print(ROOT_DIR4)
    # Working
    stocksCSV = os.path.join(str(ROOT_DIR4), "stocks_B3dfs/")
    print(stocksCSV)
    
    # TODO: implement with ROOT_DIR4
    if not os.path.exists(stocksCSV):
        # create pickle files reference strings
        pickSP500Stocks = os.path.join(str(ROOT_DIR4), "stocks_dfs/sp500tickers.pickle")
        pickB3Stocks = os.path.join(str(ROOT_DIR4), "stocks_B3dfs/b3tickers.pickle")
        # create directories reference strings 
        dirSP500Stocks = os.path.join(str(ROOT_DIR4), "stocks_dfs/")
        dirB3Stocks = os.path.join(str(ROOT_DIR4), "stocks_B3dfs/")

        # load getDataB3Stocks()
        getDataB3Stocks(pickB3Stocks, dirB3Stocks)  

        # load getDataSP500Stocks()
        getDataSP500Stocks(pickSP500Stocks, dirSP500Stocks)
        
        # call getSP500Stocks() and save it to a variable called tickers
        getSP500Stocks(pickSP500Stocks)
        
        # call getSP500Stocks() and save it to a variable called tickers
        getB3Stocks(pickB3Stocks)
        
        # call condenseData()        
        #condenseData()
    
    # return template to render
    return render_template("home.html", text = requirementsText, messageHead = messageHead, message = messageBody)
#####################################################################
#
#                                                  About Render Route 
#####################################################################
@mainBP.route('/about/')
def about():
    #
    messageHead = "Welcome my Full Stack Test App!"
    messageBody = "I hope you have a good time here. Please, take some time to leave your opinion about the features offered here. I'd really appreciate that!"
    return render_template("about.html", messageHead = messageHead, message = messageBody)
#############           end about route         ###################

#######################################################################
#
#
#                                                   Heights Render Page 
#######################################################################
# routes from form to send email with average heights
@mainBP.route("/heights/")
def heights():
    # message data to modal
    messageHead = "What About Human's Measurements?"
    messageBody = "Welcome to the page presenting some curiosities about human measurements!"
    
    # current script directory
    script_dir = os.path.dirname(__file__)
    # /app18_Admin2/app18/
    ROOT_DIR4 = Path(__file__).parent.parent
    print(ROOT_DIR4)
    heightsCSV = os.path.join(str(ROOT_DIR4), "heights_dfs/NCD_RisC_eLife_2016_height_age18_countries.csv")
    heightsDF = pd.read_csv(heightsCSV)
    dfDescription = heightsDF.describe()
    
    print(dfDescription)
    print(heightsDF.head(10))
    print(heightsDF.tail(10))
    return render_template("heights.html", messageHead = messageHead, message = messageBody)
#############          end heights route        ###################
######################3333#############################################
#
#
#                                                     Success Send Mail 
#######################################################################
@mainBP.route("/success/", methods = ["POST"])
def success():
    
    returnStatus = True
    
    from app18 import db
    
    if request.method == "POST":
        email = request.form["email_name"]
        country = request.form["country_name"]
        height = request.form["height_name"]
        
        print(email, height)
        
        if db.session.query(Data).filter(Data.email == email).count()== 0:
            
            data = Data(email, height, country)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height)).scalar()
            average_height = round(average_height, 1)
            count = db.session.query(Data.height).count()
            send_email(email, height, average_height, count)
            
            print(average_height)
            messageHead = "Hey!!!"
            messageBody = "A message was sent to the informed address ({})! Thank you for your contribution!!!".format(email)
            
            return render_template("heights.html", messageHead = messageHead, message = messageBody)
        
    messageHead = "Sorry!!! "
    messageBody = "We got something from that email ({}), already.  Only one measure for e-mail address is allowed!".format(email)
    return render_template('heights.html', 
                           messageHead = messageHead, 
                           message = messageBody, 
                           returnStatus = returnStatus)
#############         end succsess  route       ###################