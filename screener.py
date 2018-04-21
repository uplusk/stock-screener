# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 11:16:43 2018

@author: 133924
"""

from ipywidgets import widgets
import requests
import json
import time
from io import StringIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from bs4 import BeautifulSoup

import quandl
quandl.ApiConfig.api_key = "your Quandl API key" #set API key

plt.rcParams['figure.figsize']=(20,10)
plt.style.use('ggplot')
now = datetime.datetime.now()

#This class contains all the methods for fundamentals
class Fundamentals():
    def __init__(self):
        self.pre_screener = "https://www.screener.in/company/"
        self.pre_traview = "https://in.tradingview.com/symbols/"
         
    def get_screener(self, symbol):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_driver = os.getcwd() +"\\chromedriver.exe"
        
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        driver.get(self.pre_screener+symbol+"/")
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        fund_box = soup.find_all('h4', attrs={'class': 'col-sm-4'})
        fund_box = fund_box[:-5]

        stat_box = soup.find_all('dl', attrs={'class': 'dl-horizontal'})

        for fund in fund_box:
            fund_val = fund.text.strip()
            print(fund_val)

        print('\n')

        #Statistics
        comp_sales_growth_box = stat_box[0]
        comp_profit_growth_box = stat_box[1]
        roe_box = stat_box[2]

        comp_sales = []
        comp_sale_years = []
        comp_profits = []
        comp_profit_years = []
        roe = []
        roe_years = []

        #Compounded Sales Growth
        sale_years = comp_sales_growth_box.find_all('dt', attrs={'class': 'upper'})
        sales = comp_sales_growth_box.find_all('dd')

        for year in sale_years:
            year_val = year.text.strip()
            comp_sale_years.append(year_val)

        for sale in sales:
            sale_val = sale.text.strip()
            comp_sales.append(sale_val)

        sales_growth = set(zip(comp_sale_years,comp_sales))
        print("Compounded Sales Growth: ",sales_growth)

        print('\n')

        #Compounded Profit Growth
        profit_years = comp_profit_growth_box.find_all('dt', attrs={'class': 'upper'})
        profits = comp_profit_growth_box.find_all('dd')

        for year in profit_years:
            year_val = year.text.strip()
            comp_profit_years.append(year_val)

        for profit in profits:
            profit_val = profit.text.strip()
            comp_profits.append(profit_val)

        profits_growth = set(zip(comp_profit_years,comp_profits))
        print("Compounded Profits Growth: ",profits_growth)
        print('\n')

        #Return on Equity
        roe_years_vals = roe_box.find_all('dt', attrs={'class': 'upper'})
        roe_vals = roe_box.find_all('dd')

        for year in roe_years_vals:
            year_val = year.text.strip()
            roe_years.append(year_val)

        for roes in roe_vals:
            roe_val = roes.text.strip()
            roe.append(roe_val)

        roe_total = set(zip(roe_years,roe))
        print("Return on equity: ",roe_total)
  
        
    def get_traview(self,exchange,symbol):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_driver = os.getcwd() +"\\chromedriver.exe"
        
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        driver.get(self.pre_traview+exchange+"-"+symbol+"/")
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        
        columns = soup.find_all('div', attrs={'class': 'tv-widget-fundamentals__column'})
        row_list = []
        for col in columns:
            title = col.find('div', attrs={'class': 'tv-widget-fundamentals__title'}).text.strip()
            rows = col.find_all('div', attrs={'class': 'tv-widget-fundamentals__row'})
            for row in rows:
                row_val = row.text.strip()
                row_list.append(row_val)
            combined = (title,row_list)
            print(combined)
            print('\n') 

#This contains all the methods to scrape and pull data from Alphavantage
class AlphaFinanceAPI():
    def __init__(self):
        self.prefix = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
        self.daily = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
        self.interval = "1min"
        self.outputsize = "full"
        self.api_key = "Alphavantage API key"
        self.datatype = "csv"
        
    def get(self,symbol):
        url = self.prefix + "%s"%(symbol) + "&interval=" + self.interval + "&apikey=" + self.api_key
        res = requests.get(url)
        if res.status_code in (200,):
            fin_data = json.loads(res.content)
            timestamps = list(fin_data['Time Series (1min)'].keys())
            return fin_data['Time Series (1min)'][timestamps[0]]
    
    def get_historical(self,exchange,symbol):
        url = self.daily + "%s"%(symbol) + "&outputsize=" + self.outputsize + "&datatype=" + self.datatype + "&apikey=" + self.api_key
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            df = pd.read_csv(StringIO(decoded_content))
            df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            df['Date'] = pd.to_datetime(df['Date'])
            df = df[df['Date'] > pd.to_datetime("2013-03-31")]
            df.set_index('Date',inplace = True)
            df = df.reindex(index=df.index[::-1])
            return df

#Quandl has all the methods to get historical stock data and plot candlestick chart
class Quandl():
    def get_historical(self,exchange,symbol,start_date = (2013, 4, 1), end_date = None):
        start_date = datetime.date(*start_date)
        if end_date:
            end_date = datetime.date(*end_date)
        else:
            end_date = datetime.date.today()
        
        stock_hist = quandl.get(exchange+'/'+symbol, start_date=start_date, end_date=end_date)
        return stock_hist
    
    def plot(self, df):
        df['Date'] = df.index.map(mdates.date2num)
        ohlc = df[['Date','Open','High','Low','Close']]
        fig, ax = plt.subplots(figsize = (30,15))

    # plot the candlesticks
        candlestick_ohlc(ax, ohlc.values, width=1.0, colorup='green', colordown='red')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        plt.show()

#Technical Indicators
class TechIndicators():
    
    def __init__(self):
        self.cci_days = 20
        self.rsi_period = 14
        self.ewma_span = 15
        self.ewma_fast = 12
        self.ewma_slow = 26
        self.ewma_signal = 9
    
    def CCI(self, data):
        TP = (data['High'] + data['Low'] + data['Close'])/3
        CCI = pd.Series((TP - TP.rolling(window = self.cci_days, center = False).mean()) / (0.015 * TP.rolling(window = self.cci_days, center = False).std()),name = 'CCI') 
        data = data.join(CCI)
        return data['CCI']
        
    def RSI(self, data):
        delta = data['Close'].diff()
        delta = delta[1:]
       
        up, down = delta.copy(), delta.copy()
        up[up<0] = 0
        down[down>0] = 0
       
        upi = pd.ewma(up,self.rsi_period)
        doi = pd.ewma(down.abs(),self.rsi_period)
        RS = upi/doi
        data['RSI'] = 100-100/(1+RS)
        return data['RSI']
    
    def EWMA(self, df):
        df['EWMA'] = pd.ewma(df['Close'], span = self.ewma_span)
        df['Close'].plot(title='EWMA',figsize=(20,10),label='Close Price')
        df['EWMA'].plot(label='EWMA')
        plt.legend()
        
    def MACD(self, df):
        ema_fast = pd.ewma(df['Close'], span=self.ewma_fast)
        ema_slow = pd.ewma(df['Close'], span=self.ewma_slow)
        df['MACD'] = ema_fast - ema_slow
        macd_signal= pd.ewma(df['MACD'], span=self.ewma_signal)
        macd_diff = df['MACD'] - macd_signal
        
        f1, ax1 = plt.subplots(figsize = (12,8))
        ax1.plot(df.index, df['Close'], color = 'black', lw=2, label='Close')
        ax1.plot(df.index, ema_slow, color ='blue', lw=1, label='EMA(26)')
        ax1.plot(df.index, ema_fast, color ='red', lw=1, label='EMA(12)')
        
        f2, ax2 = plt.subplots(figsize = (12,8))
        ax2.plot(df.index, df['MACD'], color='green', lw=1,label='MACD Line(26,12)')
        ax2.plot(df.index, macd_signal, color='purple', lw=1, label='Signal Line(9)')
        ax2.fill_between(df.index, macd_diff, color = 'gray', alpha=0.5, label='MACD Histogram')
    
        ax1.legend(loc='upper right')
        ax1.set(title = 'Stock Price', ylabel = 'Price')
        ax2.set(title = 'MACD(26,12,9)', ylabel='MACD')
        ax2.legend(loc = 'upper right')
        ax2.grid(False)

        plt.show()
        
    def plot(self,df,t1):
        fig = plt.figure(figsize = (20,10))
        ax = fig.add_subplot(2, 1, 1)
        ax.set_xticklabels([])
        plt.plot(df['Close'],lw=1)
        plt.title('Technical Indicators: '+t1.name)
        plt.ylabel('Close Price')
        plt.grid(True)
        
        bx = fig.add_subplot(2, 1, 2)
        plt.plot(t1,'k',lw=0.75,linestyle='-',label=t1.name)
        plt.legend(loc=2,prop={'size':9.5})
        plt.ylabel(t1.name+' val')
        plt.grid(True)
        plt.setp(plt.gca().get_xticklabels(), rotation=30)

class Utils():
    @staticmethod
    def choose_exchange(exchange):
        q = Quandl()
        a = AlphaFinanceAPI()
        if exchange.upper() == "NYSE" or exchange.upper() == "NASDAQ":
            return a
        else:
            return q
            
