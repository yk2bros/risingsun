import os
from fyers_api import accessToken
from fyers_api import fyersModel
import webbrowser
import timer
import pandas
import talib
import numpy as np
import mysql.connector
import pandas_ta as ta
import pandas_ta as shubham
from mysql.connector import Error, cursor
import time
import main

high = np.array(main.high_values)
low = np.array(main.low_values)
close = np.array(main.close_values)
real = talib.ATR(high, low, close, 3)

dataFrame_high = pandas.DataFrame(high)
dataFrame_low = pandas.DataFrame(low)
dataFrame_close = pandas.DataFrame(close)

# def supertrend_up(high, low, multiplier, ATR):
#     up = ((high + low) / 2) + (multiplier * ATR)
#     return up
#
#
# def supertrend_down(high, low, multiplier, ATR):
#     down = ((high + low) / 2) - (multiplier * ATR)
#     return down


# x = 3
#
# print(real)
# print(supertrend_up(high[-1], low[-1], x, real[-1]))
# print(supertrend_down(high[-1], low[-1], x, real[-1]))
# print(len(high))

dataframe_data = pandas.DataFrame({"HIGH": high, "LOW": low, "CLOSE": close})
# print(dataframe_data)
dataframe_data.to_excel('nai_file.xlsx', sheet_name='sheet1', index=False)

# print(dataframe_data)

import pandas as pd
import numpy as np


def Supertrend(df, atr_period, multiplier):
    high = df['HIGH']
    low = df['LOW']
    close = df['CLOSE']

    # calculate ATR
    price_diffs = [high - low,
                   high - close.shift(),
                   close.shift() - low]
    true_range = pd.concat(price_diffs, axis=1)
    true_range = true_range.abs().max(axis=1)
    # default ATR calculation in supertrend indicator
    atr = true_range.ewm(alpha=1 / atr_period, min_periods=atr_period).mean()
    # df['atr'] = df['tr'].rolling(atr_period).mean()

    # HL2 is simply the average of high and low prices
    hl2 = (high + low) / 2
    # upperband and lowerband calculation
    # notice that final bands are set to be equal to the respective bands
    final_upperband = upperband = hl2 + (multiplier * atr)
    final_lowerband = lowerband = hl2 - (multiplier * atr)

    # initialize Supertrend column to True
    supertrend = [True] * len(df)

    for i in range(1, len(df.index)):
        curr, prev = i, i - 1

        # if current close price crosses above upperband
        if close[curr] > final_upperband[prev]:
            supertrend[curr] = True
        # if current close price crosses below lowerband
        elif close[curr] < final_lowerband[prev]:
            supertrend[curr] = False
        # else, the trend continues
        else:
            supertrend[curr] = supertrend[prev]

            # adjustment to the final bands
            if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                final_lowerband[curr] = final_lowerband[prev]
            if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                final_upperband[curr] = final_upperband[prev]

        # to remove bands according to the trend direction
        if supertrend[curr] == True:
            final_upperband[curr] = np.nan
        else:
            final_lowerband[curr] = np.nan

    return pd.DataFrame({
        'Supertrend': supertrend,
        'Final Lowerband': final_lowerband,
        'Final Upperband': final_upperband
    }, index=df.index)


# print(Supertrend(dataframe_data, 3, 3).to_string())
Supertrend(dataframe_data, 3, 3).to_excel("super_tren_d.xlsx", sheet_name='sheet2', index=False)

# print(Supertrend(dataframe_data, 3, 3).tail(1)["Final Lowerband"][len(Supertrend(dataframe_data, 3, 3)) - 1])
# print(Supertrend(dataframe_data, 3, 3).tail(1)["Supertrend"][len(Supertrend(dataframe_data, 3, 3)) - 1])
# print(main.close_values[len(main.close_values) - 1])

a = main.close_values[len(main.close_values) - 1]
b = Supertrend(dataframe_data, 3, 3).tail(1)["Final Lowerband"][len(Supertrend(dataframe_data, 3, 3)) - 1]
c = Supertrend(dataframe_data, 3, 3).tail(1)["Supertrend"][len(Supertrend(dataframe_data, 3, 3)) - 1]

d = Supertrend(dataframe_data, 3, 3).tail(1)["Final Upperband"][len(Supertrend(dataframe_data, 3, 3)) - 1]

dema = talib.DEMA(np.array(main.close_values), timeperiod=3)
print(dema[-1])
print(main.close_values[-1])
print(type(c))
index = len(Supertrend(dataframe_data,3,3))
print(index)
flag = False
counter  = 0
for i in range(index):
    if Supertrend(dataframe_data,3,3)["Supertrend"][i] and main.close_values[i] > dema[i]and not flag:
        print("Buy")
        counter += 1
        flag = True
    elif not Supertrend(dataframe_data,3,3)["Supertrend"][i]:
        print("Sell")
        flag = False

print("Hogaya")
print(counter)