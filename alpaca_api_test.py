import alpaca_trade_api as tradeapi

api = tradeapi.REST(
    'PKYCNKMK7Z5PDI03LP6T',
    'U2zE5du9WgZgPocX00l2RLV/Ujr7ORysMFVZaWcw',
    'https://paper-api.alpaca.markets'
)

# Get our account information.
account = api.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

# Check our current balance vs. our balance at the last market close
balance_change = float(account.equity) - float(account.last_equity)
balance_change_percent = ((float(account.equity) - float(account.last_equity)) / float(account.last_equity)) * 100
print(f'Today\'s portfolio balance change: ${balance_change}')
print(f'Today\'s portfolio percent change: {balance_change_percent}%')

# Get a list of all active assets.
active_assets = api.list_assets(status='active')
# print(active_assets)

# Filter the assets down to just those on NASDAQ.
nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ' and a.symbol == 'AMZN']
# print(nasdaq_assets)

# Check if AAPL is tradable on the Alpaca platform.
aapl_asset = api.get_asset('AAPL')
if aapl_asset.tradable:
    print('We can trade AAPL.')

# Get daily price data for AAPL over the last 5 trading days.
barset = api.get_barset('AAPL', 'minute', limit=5)
aapl_bars = barset['AAPL']

# See how much AAPL moved in that timeframe.
week_open = aapl_bars[0].o
week_close = aapl_bars[-1].c
percent_change = (week_close - week_open) / week_open * 100
print('AAPL moved {}% over the last 5 days'.format(percent_change))

# Check if the market is open now.
clock = api.get_clock()
print('The market is {}'.format('open.' if clock.is_open else 'closed.'))
