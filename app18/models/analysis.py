'''
Created on Jul 13, 2019

@author: franklincarrilho
'''
from flask import Blueprint, render_template, request
from pandas_datareader import data
from dateutil.relativedelta import relativedelta
import datetime
from datetime import date, time
import yfinance as yf
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sea
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.layouts import gridplot, Box
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import HoverTool, LayoutDOM, NumeralTickFormatter, Legend, LegendItem
# for Yahoo stock detail
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import ast
import os
from urllib.request import Request, urlopen

analysisBP = Blueprint("analysis", __name__, 
                 template_folder = "templates",
                 static_folder = "static")

# For ignoring SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# function to get user stock data adapted from Abhisek Roy on April 25, 2019
# https://www.promptcloud.com/blog/how-to-scrape-yahoo-finance-data-using-python/
def getStockInfo(tickerToSearch):
    '''
    '''
    urlYahooFinance = "https://in.finance.yahoo.com/quote/" + tickerToSearch + "?ltr=1"
    reqYahooFinance = Request(urlYahooFinance, headers = {"User-Agent": "Mozilla/5.0"})
    requestedPageOp =urlopen(reqYahooFinance).read()
    
    tickerSoupRawDt = BeautifulSoup(requestedPageOp, "html.parser")
#     tickerHtmlData  = tickerSoupRawDt.prettify("utf-8") # for final html file
    tickerJsonData  = {}
    tickerDetails   = {}
    
    for span in tickerSoupRawDt.findAll("span", 
                                        attrs = {"class": "Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)"}):
        tickerJsonData["PRESENT_VALUE"] = span.text.strip()
    
    for div in tickerSoupRawDt.findAll('div', attrs={'class': 'D(ib) Va(t)'}):
        for span in div.findAll('span', recursive=False):
            tickerJsonData['PRESENT_GROWTH'] = span.text.strip()
    
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'PREV_CLOSE-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['PREV_CLOSE'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'OPEN-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['OPEN'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'BID-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['BID'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'ASK-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['ASK'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'DAYS_RANGE-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['DAYS_RANGE'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'FIFTY_TWO_WK_RANGE-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['FIFTY_TWO_WK_RANGE'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'TD_VOLUME-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['TD_VOLUME'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'AVERAGE_VOLUME_3MONTH-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['AVERAGE_VOLUME_3MONTH'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'MARKET_CAP-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['MARKET_CAP'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'BETA_3Y-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['BETA_3Y'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'PE_RATIO-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['PE_RATIO'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'EPS_RATIO-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['EPS_RATIO'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'EARNINGS_DATE-value'}):
        tickerDetails['EARNINGS_DATE'] = []
        for span in td.findAll('span', recursive=False):
            tickerDetails['EARNINGS_DATE'].append(span.text.strip())
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'DIVIDEND_AND_YIELD-value'}):
        tickerDetails['DIVIDEND_AND_YIELD'] = td.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'EX_DIVIDEND_DATE-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['EX_DIVIDEND_DATE'] = span.text.strip()
    for td in tickerSoupRawDt.findAll('td', attrs={'data-test': 'ONE_YEAR_TARGET_PRICE-value'}):
        for span in td.findAll('span', recursive=False):
            tickerDetails['ONE_YEAR_TARGET_PRICE'] = span.text.strip()
            
#     tickerJsonData['OTHER_DETAILS'] = tickerDetails 
    
    return tickerJsonData, tickerDetails

#####################################################################
#
#
#                                                   Investments Route
#####################################################################   
@analysisBP.route('/plot/', methods = ["POST", "GET"])
def plot():
    '''Plot function using bokeh library'''
            
    # check whether it was submitted by the form
    if request.method == "POST":
        #
        messageHead = "Symbol Found!"
        messageBody = "Please, take some time to leave your opinion about the features offered here. I'd really appreciate that!"
        stringInitialDate = request.form["initialDate"]
        stringFinalDate = request.form["finalDate"]
        # convert to datetime process
        startDate = datetime.datetime(int(stringInitialDate[-4:]),
                                      int(stringInitialDate[0:2]),
                                      int(stringInitialDate[3:5]))
        endDate = datetime.datetime(int(stringFinalDate[-4:]),
                                    int(stringFinalDate[0:2]),
                                    int(stringFinalDate[3:5]))
        tickerToSearch = request.form["tickerToSearch"]

        print(startDate)
        print(endDate)
    else:
        #
        messageHead = "Welcome to the Investments Page!"
        messageBody = "I hope you have a good time here. Please, take some time to leave your opinion about the features offered here. I'd really appreciate that!"
        tickerToSearch = "GOOG"
        startDate = datetime.datetime(2020,3,10)
        endDate = datetime.datetime(2021,3,10)
        print(startDate)
        print(endDate)
    
    # get stock detail
    tickerDetailsInfo, tickerDetailsInfo2 = getStockInfo(tickerToSearch)
    for detail, value in tickerDetailsInfo.items():
        print("\n", detail, "=", value)
        for detail2, val2 in tickerDetailsInfo2.items():
            print("\n", detail2, "=", val2)
        
    # dataframe generating data
    try:
        df = data.get_data_yahoo(tickerToSearch, start = startDate, end = endDate)
        dfAnalysis = data.get_data_yahoo(tickerToSearch, start = date.today() - relativedelta(years=1), end = date.today())
    except Exception as error:
        messageHead = "Sorry!!!"
        messageBody = "The informed symbol doesn't have a match in the Yahoo Finance database. Please, check the symbol for the stock to search and try again. Thank you!"
        # return values for rendering
        return render_template("plot.html", messageHead = messageHead, message = messageBody)
        
    # function to determine whether oscillation is positive, negative or inexistent
    def valueStatus(closevalue, openvalue):
        if closevalue > openvalue:
            value="Positive"
        elif closevalue < openvalue:
            value="Negative"
        else:
            value="NoChange"
        return value
    
    # add three new columns to the df dataframe
    df["CloseStatus"] = [valueStatus(closeValue, openValue) for closeValue, openValue in zip(df.Close, df.Open)]
    df["AverageValue"] = (df.Open + df.Close)/2
    df["Variation"] = abs(df.Close - df.Open)
    
    print(df)
    
    # tools
    TOOLS = "crosshair, pan, wheel_zoom, box_zoom, reset"
    
    # bokeh plot 01
    plotFigure = figure(tools = TOOLS, x_axis_type = "datetime",
                        width = 900,
                        height = 300, 
                        sizing_mode = "scale_both")
    
    # 
    plotFigure.yaxis.formatter = NumeralTickFormatter(format = "0.00")
    
    # handle graph title error 
    try:
    # localhost title for the graph
        plotFigure.title= "Candlestick Chart for "+tickerToSearch+" (from "+startDate.strftime("%Y/%m/%d")+" to "+endDate.strftime("%Y/%m/%d")+")"
    # remote title for the graph
    except:
        plotFigure.title.text = "Candlestick Chart for "+tickerToSearch+" (from "+startDate.strftime("%Y/%m/%d")+" to "+endDate.strftime("%Y/%m/%d")+")"
    
    plotFigure.grid.grid_line_alpha = 0.5

    # determine plotFigure rectangle coordinate
    hours_12 = 12*60*60*1000
    #
    toolTipSourceP = ColumnDataSource(data = dict(Open = df["Open"], 
                                                 High = df["High"], 
                                                 Low = df["Low"], 
                                                 Close = df["Close"]))
    #
    print(df.columns)
    
    # define tooltips column data source
    toolTipSource = ColumnDataSource(data = dict(Date = df.index, 
                                                 Open = df.Open, 
                                                 High = df.High, 
                                                 Variation = df.Variation,
                                                 Low = df.Low, 
                                                 Close = df.Close))
#     toolTipSource = ColumnDataSource(df)
#     print(toolTipSource.data.keys())

    # invisible rectangle for tooltips
    plotFigure.rect(df.index[df.CloseStatus=="Positive"], 
                    df.AverageValue[df.CloseStatus=="Positive"], 
                    hours_12, 
                    df.Variation[df.CloseStatus=="Positive"], 
                    fill_alpha = 0.2, 
                    fill_color = None, 
                    line_color = None)
    
    # segments definition
    plotFigure.segment(df.index,
                       df.High,
                       df.index,
                       df.Low,
                       color="Black")
    # positive rectangles definition
    plotFigure.rect(df.index[df.CloseStatus=="Positive"],
                    df.AverageValue[df.CloseStatus=="Positive"],
                    hours_12, 
                    df.Variation[df.CloseStatus=="Positive"],
                    fill_color="#CCFFFF",
                    line_color="black")
    # negative rectangles definition
    plotFigure.rect(df.index[df.CloseStatus=="Negative"],
                    df.AverageValue[df.CloseStatus=="Negative"],
                    hours_12, 
                    df.Variation[df.CloseStatus=="Negative"],
                    fill_color="Red",
                    line_color="black")

    # draw close prices line
    plotFigure.line(df.index, df['Close'], color='navy', alpha=0.5, legend = "Close")
    
    # create tool tips
    toolTips = [("Date ", "@Date"), 
                ("Open ", "@Open{0,0.00}"), 
                ("High ", "@High{0,0.00}"), 
                ("Low ", "@Low{0,0.00}"), 
                ("Close ", "@Close{0,0.00}")]
    #
    toolTFormatters = {"Date":"datetime", 
                       "Open":"printf", 
                       "High":"printf", 
                       "Low":"printf", 
                       "Close":"printf"}
    # add labels
    plotFigure.yaxis.axis_label = "Prices ($)"
    
    # add legend
    legend = Legend(items = [])
    
    plotFigure.legend.title = tickerToSearch
    plotFigure.legend.location = "top_left"
    plotFigure.legend.title_text_font_style = "bold"
    plotFigure.legend.title_text_font_size = "15pt"
    
    #
#     plotFigure.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
#     plotFigure.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
#     plotFigure.xaxis.major_label_text_color = None  #note that this leaves space between the axis and the axis label
    plotFigure.xaxis.visible = False
    
    # bokeh plot 02
    plotFigure1 = figure(x_axis_type = "datetime",
                        width = 900,
                        height = 150, 
                        sizing_mode = "scale_both")
    #
        # draw close prices line
    plotFigure1.line(df.index, 
                     df['Volume'], 
                     color='navy', 
                     alpha=0.5)
    
    # determine range
    plotFigure1.x_range = plotFigure.x_range
    
    # add labels
    plotFigure1.xaxis.axis_label = "Dates"
    plotFigure1.yaxis.axis_label = "Volume"
    
    #
    plotFigure1.yaxis.formatter = NumeralTickFormatter(format = "0 a")
    
    # add tool tips
    plotFigure1.add_tools(HoverTool(tooltips = toolTips))
    
    # compose the plot 
    # without griplot
    plots = (plotFigure, plotFigure1)
    # with griplot
    plots2 = gridplot([[plotFigure], [plotFigure1]], merge_tools = False)
#     show(plots2)
    
    (script1, div1) = components(plots)
       
    # js and css files to include in the head of plot.html file
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
        
    # return values for rendering
    return render_template("plot.html", 
                           script1 = script1,
                           div1 = div1,
                           cdn_css = cdn_css, 
                           cdn_js = cdn_js, 
                           messageHead = messageHead, 
                           message = messageBody)

    # output_file("candleStick.html")
    # show(plotFigure)
#############       end investments route       ################### 

######      get stock detail from yahoo-fianace API         #######


