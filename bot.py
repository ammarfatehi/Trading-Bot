# alpaca
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

# red white blue strategy

emasUsed = [3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60]

for ema in emasUsed:
    df['Ema_' + str(ema)] = round(df.iloc[:, 4].ewm(span=ema, adjust=False).mean(), 2)  # this gives us the exponential moving average

print(df.iloc[-1]['Adj Close'])

pos = 0
num = 0
percent_change = []
for i in df.index:
    cmin = min(df['Ema_3'][i], df['Ema_5'][i], df['Ema_8'][i], df['Ema_10'][i], df['Ema_12'][i], df['Ema_15'][i])
    cmax = max(df['Ema_30'][i], df['Ema_35'][i], df['Ema_40'][i], df['Ema_45'][i], df['Ema_50'][i], df['Ema_60'][i])
    close = df['Adj Close'][i]

    if cmin > cmax:
        # print('red white blue')
        if pos == 0:
            bp = close  # bp is the buy price so if we have a rwb we are setting our buy price to the closing price
            pos = 1  # when pos is 1 that mean we currently have a position
            print(f'buying now at: {bp}')

    elif cmin < cmax:
        # print('blue white red')
        if pos == 1:
            pos = 0  # resting pos
            sp = close  # selling price
            print(f'selling now at: {sp}')
            pc = (sp / bp - 1) * 100  # percent change on current position
            percent_change.append(pc)

    if num == df[
        'Adj Close'].count() - 1 and pos == 1:  # this checks if we are at the end of our df and still have a position, so we must sell
        pos = 0  # resting pos
        sp = close  # selling price
        print(f'selling now at: {sp}')
        pc = (sp / bp - 1) * 100  # percent change on current position
        percent_change.append(pc)

    num += 1  # keeps track where we are in the dataframe

print(percent_change)

gains = 0
ng = 0
losses = 0
nl = 0
totalR = 1
for percent in percent_change:
    if percent > 0:
        gains += percent
        ng += 1
    else:
        losses += percent
        nl += 1
    totalR = totalR * (percent / 100 + 1)
totalR = round((totalR - 1) * 100, 2)

if ng > 0:
    avg_gain = gains / ng
    maxR = str(max(percent_change))  # this finds the highest percent gain trade
else:
    avg_gain = 0
    maxR = 'undefined'

if nl > 0:
    avg_loss = losses / nl
    maxL = str(min(percent_change))
    ratio = str(-avg_gain / avg_loss)  # risk reward relationship
else:
    avg_loss = 0
    maxL = 'undefined'
    ratio = 'infinite'

if ng > 0 or nl > 0:
    batting_avg = ng / (ng + nl)
else:
    batting_avg = 0

# giving stats to user
print()
print("Results for "+ ticker +" going back to "+str(df.index[0])+", Sample size: "+str(ng+nl)+" trades")
print("EMAs used: "+str(emasUsed))
print("Batting Avg: "+ str(batting_avg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avg_gain))
print("Average Loss: "+ str(avg_loss))
print("Max Return: "+ maxR)
print("Max Loss: "+ maxL)
print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" )
# print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
print()

