import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
import datetime as dt

ticker = input('enter stock: ')
yf.pdr_override()

start_year = 2019
start_month = 1
start_day = 1
start = dt.datetime(start_year, start_month, start_month)
now = dt.datetime.now()
df = pdr.get_data_yahoo(ticker, start, now)
print(df.iloc[-1])
print(yf.Ticker(ticker).history(period='2d')['Close'][-1])