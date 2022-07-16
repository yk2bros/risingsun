import os
from fyers_api import accessToken
from fyers_api import fyersModel
import webbrowser
import timer
import pandas
import talib
import numpy
import mysql.connector
import pandas_ta
from mysql.connector import Error, cursor
import time

app_id = "JBGZVR59OA-100"
secret_key = "CNMXMDL77L"
redirect_uri = "https://www.google.com/"
response_type = "code"
grant_type = "authorization_code"


def get_access_token():
    if not os.path.exists("access_token.txt"):

        session = accessToken.SessionModel(client_id=app_id, secret_key=secret_key, redirect_uri=redirect_uri,
                                           response_type=response_type, grant_type=grant_type)
        response = session.generate_authcode()
        webbrowser.open(response)
        auth_code = input("Enter Auth Code: ")
        session.set_token(auth_code)
        access_token = session.generate_token()["access_token"]
        with open("access_token.txt", "w") as f:
            f.write(access_token)
    else:
        with open("access_token.txt", "r") as f:
            access_token = f.read()
    return access_token




fyers = fyersModel.FyersModel(client_id=app_id, token=get_access_token(), log_path="")

data = {"symbol": "NSE:BHARTIARTL-EQ", "resolution": "5", "date_format": "0", "range_from": f"{timer.custom_epoch(4)}",
        "range_to": f"{timer.custom_epoch(0)}", "cont_flag": "1"}



# print(fyers.history(data))


json_file = fyers.history(data)
close_values= []
open_values = []
high_values = []
low_values = []
for i in range(len(json_file["candles"])):
    close_values.append(json_file["candles"][i][4])


for i in range(len(json_file["candles"])):
    low_values.append(json_file["candles"][i][3])


for i in range(len(json_file["candles"])):
    high_values.append(json_file["candles"][i][2])


for i in range(len(json_file["candles"])):
    open_values.append(json_file["candles"][i][1])

#
# print("CLOSE ", close_values, "\n\n\n\n")
# print("LOW ", low_values, "\n\n\n\n\n")
# print("HIGH ", high_values, "\n\n\n\n\n")
# print("OPEN ",open_values, "\n\n\n\n\n")
#
#
#














# print(len(json_file['candles']))
# empty_list = []
# for i in range(len(json_file["candles"])):
#         empty_list.append(json_file["candles"][i][4])
#         print(empty_list)
#         print(json_file["candles"][i][1])

# candles = pandas.DataFrame(fyers.history(data))
# # candles.to_excel('sample_data.xlsx', sheet_name='sheet1', index=False)
# print(candles)
# print("Export successfully")
# print(empty_list)
# real = talib.DEMA(numpy.array(empty_list),timeperiod=30)



# #database connection
# connection = mysql.connector.connect(user='root', password='root',
#                                      host='localhost',
#                                      database='risingsun')
# pointer = connection.cursor()
# # pointer.execute("INSERT INTO closevalues(closevalues) VALUES (6000.500)")