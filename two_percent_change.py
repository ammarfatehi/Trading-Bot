import alpaca_trade_api as tradeapi

API_KEY = 'PKXO3X5VT3J93OATDLHZ'
SECRET_KEY = 'e2JidMwKh8iLUDicyL9/bt3aiw28FrdpfI2neDNz'
api = tradeapi.REST(API_KEY, SECRET_KEY, 'https://paper-api.alpaca.markets',
                    api_version='v2')  # or use ENV Vars shown below
account = api.get_account()


def daily_change():
    balance_change = float(account.equity) - float(account.last_equity)
    return balance_change


def place_order(symbol, qty, side, type, time_in_force, stop_price=None, limit_price=None):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force=time_in_force,
        stop_price=stop_price
    )


def place_order_bracket(symbol, qty, side, type, time_in_force, stop_price=None, limit_price=None):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force=time_in_force,
        order_class='bracket',
        stop_loss={'stop_price': stop_price},
        take_profit={'limit_price': limit_price}
    )


def all_positions():
    return api.list_positions()


def existing_position(symbol):
    return api.get_position(symbol)


api.cancel_all_orders()
print(api.get_clock().is_open)

stocks = {}
bought = {}
sold = {}
stocks_id = {}

# getting all the symbols in QQQ
file = open('QQQ_holdings.csv').readlines()
symbols = [holding.split(',')[2].strip() for holding in file[1:]]
for symbol in symbols:
    stocks[symbol] = True

for stock in stocks:
    stocks[stock] = True
    sold[stock] = True
print(stocks)
# 2% change strategy.

# step1: buy all stocks
for stock in stocks:
    place_order(stock, 10, 'buy', 'market', 'day')

# step2: set the bought price and place stop orders to sell if price drops more than 0.5%
for stock in stocks:
    ex = existing_position(stock)
    bought[stock] = ex.avg_entry_price
    price_to_sell = float(ex.avg_entry_price) * float(1-.005)
    place_order(stock, 10, 'sell', 'stop', 'day', price_to_sell)

while True:
    print('looped')
    if api.get_clock().is_open:

        for stock, statue in stocks.items():
            if statue:
                place_order(stock, 10, 'buy', 'market', 'day')
                statue = False
                sold[stock] = True

            if sold[stock]:
                try:
                    ex = existing_position(stock)
                    bought[stock] = ex.avg_entry_price
                    stop_price = float(ex.avg_entry_price) * float(1 - .005)
                    limit_price = float(ex.avg_entry_price) * float(1.05)
                    place_order_bracket(stock, 10, 'sell', 'stop', 'day', stop_price, limit_price)
                    sold[stock] = False
                    stocks_id[stock] = ex.asset_id
                    stocks[stock] = True
                except:
                    print('no avg price yet')

                for position in api.list_positions():
                    if stock == position.symbol:
                        stocks[stock] = False

stock = 'AAPL'
ex = existing_position(stock)
bought[stock] = ex.avg_entry_price
stop_price = float(ex.avg_entry_price) * float(1 - .005)
limit_price = float(ex.avg_entry_price) * float(1.05)
place_order_bracket(stock, 10, 'buy', 'market', 'day', stop_price, limit_price)