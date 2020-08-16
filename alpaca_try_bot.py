# api key PKPFYQHJZW2UR48DD2CN
# secret key jQ926AiDOmsVjVHp1koC2xL8iEzOflLNFTMp5QJj

import json
import requests
import alpaca_trade_api as tradeapi
import yfinance as yf
from pandas_datareader import data as pdr
import datetime as dt

API_KEY = 'PKTX4DUZP7KGOT8SK3NM'
SECRET_KEY = 'UC9k2nQgqi9cm56fCZbcVBIw696ER/gCK7e1JqTl'
headers = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
BASE_URL = 'https://paper-api.alpaca.markets'
market_url = 'https://data.alpaca.markets/v1'
ACCOUNT_URL = '{}/v2/account'.format(BASE_URL)
orders_url = '{}/v2/orders'.format(BASE_URL)


def get_account():
    r = requests.get(ACCOUNT_URL, headers=headers)
    return json.loads(r.content)  # this will take the string and return it in dictionary form


def create_order(symbol, qty, side, type, time_in_force):
    data = {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': type,
        'time_in_force': time_in_force
    }
    r = requests.post(orders_url, json=data, headers=headers)
    return json.loads(r.content)


def get_orders():
    data = {
        'status': 'closed',
        'limit': 150
    }
    r = requests.get(orders_url, json=data, headers=headers)
    return json.loads(r.content)


def get_last_quote(symbol):
    last_quote = '{}/last_quote/stocks/{}'.format(market_url, symbol)
    r = requests.get(last_quote, headers=headers)
    return json.loads(r.content)


def get_bars(symbol, timeframe, start=None):
    bars = '{}/v1/bars/{}'.format(market_url, timeframe)
    data = {
        'symbol': symbol,
    }
    r = requests.get(bars, json=data, headers=headers)
    return json.loads(r.content)


def get_last_trade(symbol):
    last_quote = '{}/last_quote/stocks/{}'.format(market_url, symbol)
    r = requests.get(last_quote, headers=headers)
    return json.loads(r.content)


def get_asset(symbol):
    last_quote = '{}/v2/assets/{}'.format(BASE_URL, symbol)
    r = requests.get(last_quote, headers=headers)
    return json.loads(r.content)


def market_open():
    market_clock = '{}/v2/clock'.format(BASE_URL)
    r = requests.get(market_clock, headers=headers)
    return json.loads(r.content)['is_open']


stocks = {}
bought = {}
sold = {}
percent_change = {}
all_bought = False
# getting all the symbols in QQQ
file = open('QQQ_holdings.csv').readlines()
symbols = [holding.split(',')[2].strip() for holding in file[1:]]
for symbol in symbols:
    stocks[symbol] = True
print(stocks)
print(get_orders())

# 2% change strategy.

# step 1: check if market is open
while market_open():
    print('looped')
    # step 2: buy all the stocks
    if all_bought is False:
        for stock in stocks:
            response = create_order(stock, 20, 'buy', 'market', 'day')
            # print(response)

            # current_price = response["filled_avg_price"]
            # bought[stock] = current_price
            #
            # print(f'buying {stock} at {current_price}')

    all_bought = True
    print(get_orders())
    for order in get_orders():
        print('order')
        print(order['symbol'] + ' - ' + order['filled_avg_price'])

    # step 3 keep checking if the stock drops below a 1% of bought price if so sell it
    for stock in stocks:
        current_sell = get_last_quote('AAPL')['last']['askprice']
        print(stock+ ' - '+ current_sell)
        if current_sell == (bought[stock]*.99):
            response = create_order(stock, 100, 'sell', 'market', 'day')
            sell_price = response["filled_avg_price"]
            print(f'selling {stock} at {sell_price}')
            sold[stock] = sell_price
            percent_change[stock] = ((sell_price-bought[stock])/bought[stock])*100

# step 4: close all positions (gonna have to figure this one out after making sure steps 1-3 work as intended)
print(stocks)
print(bought)
print(sold)
print(percent_change)
