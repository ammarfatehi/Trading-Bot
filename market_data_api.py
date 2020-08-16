import requests
import json
import btalib

API_KEY = 'PKVFX44K5WC5QVOB0DZA'
SECRET_KEY = '/1j71yOLLY0U1xu0RMGtXkiMeyhOt7SQxjA70eBB'
headers = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
market_url = 'https://data.alpaca.markets'
bars_url = '{}/v1/bars'.format(market_url)

# getting all the symbols in QQQ
file = open('QQQ_holdings.csv').readlines()
symbols = [holding.split(',')[2].strip() for holding in file[1:]]
symbols = ','.join(symbols)
print(symbols)
day_bars_rl = '{}/{}?symbols={}&limit=1000'.format(bars_url, 'day', symbols)

r = requests.get(day_bars_rl, headers=headers)
output = json.dumps(r.json(), indent=4)
print(output)
output_file = open('output.txt','w')
output_file.write(output)