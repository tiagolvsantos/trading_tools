from src.libs import tabulate_lib

import json
from websocket import create_connection
import pandas as pd
import time

def recv_to_object(websocket):
    data = websocket.recv()
    return json.loads(data)

def epoch_to_datetime(epoch_date: int):
    if len(str(epoch_date)) > 10:
        epoch_date = str(epoch_date)[:-3]
    timeArray = time.localtime(int(epoch_date))
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

def binance_abnormal_trading():
    websocket = create_connection("wss://bstream.binance.com:9443/stream?streams=abnormaltradingnotices")
    while True:
        data = recv_to_object(websocket)
       
        df_data = pd.DataFrame([data["data"]])

        for index, row in df_data.iterrows():
            df_data.at[index,'sendTimestamp']= str(epoch_to_datetime(int(row['sendTimestamp'])))
            df_data.at[index,'priceChange']= f"{(round(float(row['priceChange']),2)*100)}%"
            tabulate_lib.tabulate_it("",df_data)
            print('\n')
   

def main():
    while True:
        binance_abnormal_trading()