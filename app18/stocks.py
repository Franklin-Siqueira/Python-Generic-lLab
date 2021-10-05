# Copyright 2021 Franklin Siqueira.
# SPDX-License-Identifier: Apache-2.0

'''
Created on Jul 12, 2019

@author: franklincarrilho
'''
from pandas_datareader import data
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date, time
import yfinance as yf
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sea
# from bokeh.plotting import figure, show, output_file, ColumnDataSource
# from bokeh.layouts import gridplot, Box
# from bokeh.embed import components
# from bokeh.resources import CDN
# from bokeh.models import HoverTool, LayoutDOM, NumeralTickFormatter, Legend, LegendItem
# import for importing WikipidiA data
import bs4 as bs
import pickle
import requests
import os
import pandas as pd
import time as tmp

# mpltLibPlot, getSP500Stocks, getB3Stocks, getDataB3Stocks, getDataSP500Stocks, condenseData

# def mpltLibPlot(figureName, dataFrameName):
#     '''
#     matplotlib to axis plot
#     **********************
#     requires: mtplotlib, pandas, seaborn
#     '''
#     mpltFigure = figureName
#     dfAnalysis = dataFrameName
#     mpltFigure, (axis1, axis2) = plt.subplots(2, 1, figsize = (16, 12))
#            
#     #relReturns = dfAnalysis.pct_change(1)
#     logReturns = np.log(dfAnalysis).diff()
#     
#     for c in logReturns:
#         axis1.plot(logReturns.index, logReturns[c].cumsum(), label = str(c))
#     
#     axis1.set_ylabel("Cumulative Log Returns")
#     axis1.legend(loc ="best")
#     
#     for c in logReturns:
#         axis2.plot(logReturns.index, 100*(np.exp(logReturns[c].cumsum())-1), label = str(c))
#     
#     axis2.set_ylabel("Total Relative Returns (%)")
#     axis2.legend(loc ="best")
#     
#     return mpltFigure

# define function to get S&P 500 data
def getSP500Stocks(pickFile):
    '''
    matplotlib 2 axis plot
    ************************
    requires: BeautifulSoup4
    '''
    response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"class":"wikitable sortable"})
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        tickers.append(ticker.rstrip("\n"))
    # write bytes to memory "wb"
    with open(pickFile, "wb") as file:
        pickle.dump(tickers, file)
    
    print(tickers)
    return tickers

# define function to get B3 data
def getB3Stocks(pickFile):
    response = requests.get("https://en.wikipedia.org/wiki/List_of_companies_listed_on_Ibovespa")
    soup = bs.BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"class":"wikitable sortable"})
    tickers = []
    for row in table.findAll("tr")[1:]:
        tickerSymbol = row.findAll("td")[1].text
        #tickerName = row.findAll("td")[1].text
        tickers.append(tickerSymbol.rstrip("\n"))
    # write bytes to memory "wb"
    with open(pickFile, "wb") as file:
        pickle.dump(tickers, file)
    
    print(tickers)
    return tickers

# getDataB3Stocks
def getDataB3Stocks(pickFile, pickDir, reLoadB3 = False):
    
    if reLoadB3 or not os.path.exists(pickDir):
        os.makedirs(pickDir)
        tickers = getB3Stocks(pickFile)
    else:
        # read bytes from memory "rb" or file
        with open(pickFile, "rb") as file:
            tickers = pickle.load(file)
    
    if not os.path.exists(pickDir):
        os.makedirs(pickDir)
        
    generalStartDate = datetime.datetime(2014, 1, 1)
    generalEndDate = date.today()
    
    stocksNumber = []
    
    for count, ticker in enumerate(tickers):
        
        stocksNumber = tickers[count:count+10]
        
        if count % 10 == 0:
            print(count)
            
        for ticker in stocksNumber:
            
            #if not os.path.exists("../stocks_B3dfs/{}.csv".format(ticker)):
            if not os.path.exists(os.path.join(pickDir, "{}.csv".format(ticker))):
                #= os.path.join(pickDir, "{}.csv".format(ticker))
                try:
                    df = data.get_data_yahoo(ticker, start = generalStartDate, end = generalEndDate)
                    # os.path.join(pickDir, "{}.csv".format(ticker))
                    # df.to_csv("../stocks_B3dfs/{}.csv".format(ticker))
                    df.to_csv(os.path.join(pickDir, "{}.csv".format(ticker)))
                except:
                    pass
                
                print("Values added to {}".format(ticker), count)

            else:
                print("Values already loaded to {}".format(ticker), count)
                #pass

# getDataSP500Stocks
def getDataSP500Stocks(pickFile, pickDir, reLoadSP500 = False):
    
    if reLoadSP500 or not os.path.exists(pickDir):
        os.makedirs(pickDir)
        tickers = getSP500Stocks(pickFile)
    else:
        # read bytes from memory "rb" or file
        with open(pickFile, "rb") as file:
            tickers = pickle.load(file)
    
    if not os.path.exists(pickDir):
        os.makedirs(pickDir)
        
    generalStartDate = datetime.datetime(2014, 1, 1)
    generalEndDate = date.today()
    
    stocksNumber = []
    
    for count, ticker in enumerate(tickers):
        
        stocksNumber = tickers[count:count+10]
        
        if count % 10 == 0:
            print(count)
            
        for ticker in stocksNumber:
            
            if not os.path.exists(os.path.join(pickDir, "{}.csv".format(ticker))):
                
                try:
                    df = data.get_data_yahoo(ticker, start = generalStartDate, end = generalEndDate)
                    df.to_csv(os.path.join(pickDir, "{}.csv".format(ticker)))
                except:
                    pass
                
                print("Values added to {}".format(ticker), count)

            else:
                #print("Values already loaded to {}".format(ticker), count)
                pass
 
# condenseData()
def condenseData():
    
    with open("../sp500tickers.pickle", "rb") as file:
        tickers = pickle.load(file)
    
    mainDf = pd.DataFrame()
    
    for count, ticker in enumerate(tickers):
        
        try:
            df = pd.read_csv("../stocks_dfs/{}.csv".format(ticker))
            df.set_index("Date", inplace = True)
            df.rename(columns = {"Adj Close":ticker}, inplace = True)
            df.drop(["Open", "High", "Low", "Close", "Volume"], 1, inplace = True)
        except:
            pass
        
        if mainDf.empty:
            
            mainDf = df
            
        else:
            
            mainDf = mainDf.merge(df, how = "outter", on = "Date")
            
        if count % 10 == 0:
            print(count)
            
    print(mainDf.head())
    mainDf.to_csv("../sp500Condensed.csv")
##################       end functions     ########################