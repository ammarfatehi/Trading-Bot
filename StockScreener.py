import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import os
from tkinter.filedialog import askopenfilename
from pandas import ExcelWriter

# Condition 1: Current Price > 150 SMA and > 200 SMA
# Condition 2: 150 SMA and > 200 SMA
# Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
# Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
# Condition 5: Current Price > 50 SMA
# Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)
# Condition 7: Current Price is within 25% of 52 week high
# Condition 8: IBD RS rating >70 and the higher the better

yf.pdr_override()
start = dt.datetime(2019, 1, 1)
now = dt.datetime.now()
file = input('Give me excel file name of data to read: ')
if len(file)<1:
    file = pd.read_excel('RichardStocks.xlsx')

file = file.head(15)
exportList = pd.DataFrame(
    columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])

for i in file.index:
    stock = str(file["Symbol"][i])
    stock = stock.strip()
    RS_Rating = file["RS Rating"][i]

    try:
        df = pdr.get_data_yahoo(stock, start, now)

        smaUsed = [50, 150, 200]
        for sma in smaUsed:
            df['SMA_' + str(sma)] = round(df.iloc[:,4].rolling(window=sma).mean(), 2)

        current_close = df['Adj Close'][-1]  # this gets the most recent adj close in the yfinance database
        moving_avg_50 = df['SMA_50'][-1]
        moving_avg_150 = df['SMA_150'][-1]
        moving_avg_200 = df['SMA_200'][-1]
        low_of52week = min(df['Adj Close'][-260:])
        high_of52week = max(df['Adj Close'][-260:])

        try:
            moving_avg_200_20past = df['SMA_200'][-20]
        except:
            moving_avg_200_20past = 0

        print('checking ' + stock)

        # Condition 1: Current Price > 150 SMA and > 200 SMA
        if current_close > moving_avg_150 and current_close > moving_avg_200:
            cond_1 = True
        else:
            cond_1 = False

        # Condition 2: 150 SMA and > 200 SMA
        if moving_avg_150 > moving_avg_200:
            cond_2 = True
        else:
            cond_2 = False

        # Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
        if moving_avg_200 > moving_avg_200_20past:
            cond_3 = True
        else:
            cond_3 = False

        # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        if moving_avg_50 > moving_avg_150 and moving_avg_50 > moving_avg_200:
            cond_4 = True
        else:
            cond_4 = False

        # Condition 5: Current Price > 50 SMA
        if current_close > moving_avg_50:
            cond_5 = True
        else:
            cond_5 = False

        # Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)
        if current_close > (low_of52week * 1.3):
            cond_6 = True
        else:
            cond_6 = False

        # Condition 7: Current Price is within 25% of 52 week high
        if current_close >= (.75 * high_of52week):
            cond_7 = True
        else:
            cond_7 = False

        # Condition 8: IBD RS rating >70 and the higher the better
        if RS_Rating > 70:
            cond_8 = True
        else:
            cond_8 = False

        # Check to make sure all conditions are true
        if cond_1 and cond_2 and cond_3 and cond_4 and cond_4 and cond_5 and cond_6 and cond_7 and cond_8:
            exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating, "50 Day MA": moving_avg_50,
                                            "150 Day Ma": moving_avg_150, "200 Day MA": moving_avg_200,
                                            "52 Week Low": low_of52week, "52 week High": high_of52week},
                                           ignore_index=True)
    except:
        print(f'no data on {stock}')
        
print(exportList)

# saving all the stocks and their df that meant our conditions into an excel file
file_path = r'C:\Users\ammar\Documents\Pyhton Projects\stock price update bot\Worked on Data\idk y i need this but i need this so my excel files are saved in this folder'
new_file = os.path.dirname(file_path)+'/Screen_Output.xlsx' # this takes the original file path and adds on the new new excel file
writer = ExcelWriter(new_file)  # this pretty much makes the new excel file
exportList.to_excel(writer, "Sheet1")   # this puts our df into sheet1 of the document
writer.save()


