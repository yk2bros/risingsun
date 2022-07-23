import time
import access_token
import numpy as np
import pandas as pd
import talib

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']

CURRENT_TIME = int(time.time())


def get_custom_epoch(days: int) -> int:
    """
    Returns the time in EPOCH format
    :param days:
    :return:epoch_time
    """
    current_time = time.time()
    seconds_in_day = days * (24 * 60 * 60)
    required_time = current_time - seconds_in_day
    return int(required_time)


def get_custom_date(days: int):
    """
    Convert EPOCH time into human-readable format
    :param days:
    :return: date
    """
    epoch_time = get_custom_epoch(days)
    year = time.localtime(epoch_time)[0]
    month = time.localtime(epoch_time)[1]
    date = time.localtime(epoch_time)[2]
    months_in_name = MONTHS[month - 1]
    return f"{date} {months_in_name}, {year}"


def pass_stock_data(stock_name: str, resolution: str, from_days: int, to_days=CURRENT_TIME, cont_flag="1",
                    date_format="0", ):
    """
    Returns the dictionary(key-value pair)
    :param stock_name:
    :param resolution:
    :param from_days:
    :param to_days:
    :param cont_flag:
    :param date_format:
    :return:data
    """
    print("\nGenerating String of Stock Meta Data")
    data = {"symbol": f"NSE:{stock_name}-EQ", "resolution": f"{resolution}", "date_format": f"{date_format}",
            "range_from": get_custom_epoch(from_days),
            "range_to": CURRENT_TIME, "cont_flag": "1"}
    print("Generated String of Stock Meta Data is - \n", data, "\n")
    return data


def get_history_data(data2: dict):
    """
    Return the dictionary which contains Stock data
    :param data2:
    :return: data
    """

    data = access_token.get_fyers_entry_point().history(data2)
    return data


def get_supertrend(df, atr_period, multiplier):
    """
    Returns the values of Supertrend
    :param df:
    :param atr_period:
    :param multiplier:
    :return: upperband and lowerband
    """
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


def get_dema(close_values: list, time_period: int):
    """
    Returns the value of DEMA
    :param close_values:
    :param time_period:
    :return: DEMA
    """

    dema = talib.DEMA(np.array(close_values), timeperiod=time_period)
    return dema.tolist()


def get_dema_last_value(close_values: list, time_period: int):
    """
    Returns the last value of DEMA
    :param close_values:
    :param time_period:
    :return: DEMA
    """

    dema = talib.DEMA(np.array(close_values), timeperiod=time_period)
    return dema[-1]


def list_to_numpy_array(list: list):
    """
    Converts list into numpy array
    :param list:
    :return: nparray
    """
    return np.array(list)


def list_to_npdf(list: list):
    """
    Converts the list in to pandas dataframe
    :param list:
    :return: pandas dataframe
    """
    numpy_list = list_to_numpy_array(list)
    return pd.DataFrame(numpy_list)