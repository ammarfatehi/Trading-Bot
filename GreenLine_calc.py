import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr

# A green line is draw every time the a stock hits a new all time high and the rest a bit and then we predict that after 3 months it will start
# rising and hit a new all time high.


yf.pdr_override()
start = dt.datetime(1980, 1, 1)
now = dt.datetime.now()
stock = input('Enter a stock: ')

while stock != 'quit':
    df = pdr.get_data_yahoo(stock, start, now)
    df.drop(df[df['Volume'] < 1000].index, inplace=True)  # this is dropping an value in our df that has a volume of less than 1k a day
    df_month = df.groupby(pd.Grouper(freq='M'))['High'].max()  # this will give us the monthly values instead of daily.

    gl_data = 0  # data of the most recent green line value
    last_glv = 0  # latest green line value
    current_data = ''  # current data of the green line value that the program will be tracking
    current_glv = 0  # current green line value we are tracking
    for index, value in df_month.items():
        if value > current_glv:
            current_glv = value
            current_data = index
            counter = 0  # will check for whether or not 3 months have past

        if value < current_glv:
            counter = counter + 1
            if counter == 3 and (index.month != now.month) or (index.year != now.year):
                if current_glv != last_glv:
                    print(current_glv)
                gl_data = current_data
                last_glv = current_glv
                counter = 0

    if last_glv == 0:
        message = stock + 'has not formed a green line yet'
    else:
        message = 'Last Green Line: '+str(last_glv) + ' on ' + str(gl_data) + ' for ' + stock
    print(message)


    stock = input('Give me a stock: ')
