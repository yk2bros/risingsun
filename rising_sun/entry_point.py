import access_token
import repository
import pandas as pd

STOCK_NAME = "SBIN"
RESOLUTION = "5"
FROM_DAYS = 10
dema_time_period = 2
OPEN_VALUES = []
HIGH_VALUES = []
LOW_VALUES = []
CLOSE_VALUES = []

# Generating Stock Details
stock_meta_data = repository.pass_stock_data(STOCK_NAME, RESOLUTION, FROM_DAYS)

# Getting the entire data of the stock
entire_stock_data = access_token.get_fyers_entry_point().history(stock_meta_data)

# length of entire stock data
print("The length of the entire stock data is = ", len(entire_stock_data['candles']), "\n")

# print
# print("The entire stock detail is - \n ", entire_stock_data)

for i in range(len((entire_stock_data)["candles"])):
    OPEN_VALUES.append((entire_stock_data)["candles"][i][1])
    HIGH_VALUES.append((entire_stock_data)["candles"][i][2])
    LOW_VALUES.append((entire_stock_data)["candles"][i][3])
    CLOSE_VALUES.append((entire_stock_data)["candles"][i][4])

dataframe_data = pd.DataFrame(
    {"HIGH": repository.list_to_numpy_array(HIGH_VALUES), "LOW": repository.list_to_numpy_array(LOW_VALUES),
     "CLOSE": repository.list_to_numpy_array(CLOSE_VALUES)})

flag = False
index = 0
quantity = 0
# for index in range(len(CLOSE_VALUES)):
#
#     if  repository.get_supertrend(dataframe_data, 3, 3)["Supertrend"][index] and CLOSE_VALUES[
#         index] > repository.get_dema(repository.list_to_numpy_array(CLOSE_VALUES),
#                                      dema_time_period)[index] :
#         print("buy")
#         flag = True
#     elif not repository.get_supertrend(dataframe_data,3,3)["Supertrend"][index] :
#         print("sell")
#         flag = False


# to print the DEMA values
# print(repository.get_dema(repository.list_to_numpy_array(CLOSE_VALUES), dema_time_period ).tolist())
# print(repository.get_dema_last_value(repository.list_to_numpy_array(CLOSE_VALUES), dema_time_period ))


# to print the supertrend values
# print((repository.get_supertrend((dataframe_data),3,3))["Supertrend"][0])
# print(len(CLOSE_VALUES))

for index in range(len(CLOSE_VALUES)):
    print(index)
    if repository.get_supertrend(dataframe_data, 3, 3)["Supertrend"][index] and CLOSE_VALUES[
        index] > repository.get_dema(repository.list_to_numpy_array(CLOSE_VALUES),
                                     dema_time_period)[index]:
        print("Buy")
        for j in range(index+1,len(CLOSE_VALUES)):
            print(j)
            if not repository.get_supertrend(dataframe_data,3,3)["Supertrend"][index]:
                print("Sell")

print("\n=================APP CLOSED=====================")
