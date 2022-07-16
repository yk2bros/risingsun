import os
from fyers_api import accessToken
from fyers_api import fyersModel
import webbrowser
import time
import timer
import pandas

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
        auth_code = input("Enter Auth COde: ")
        session.set_token(auth_code)
        access_token = session.generate_token()["access_token"]
        with open("access_token.txt", "w") as f:
            f.write(access_token)
    else:
        with open("access_token.txt", "r") as f:
            access_token = f.read()
    return access_token

print(fyersModel.FyersModel(client_id=app_id, token=get_access_token(), log_path=""))

def starter():
    return fyersModel.FyersModel(client_id=app_id, token=get_access_token(), log_path="")


