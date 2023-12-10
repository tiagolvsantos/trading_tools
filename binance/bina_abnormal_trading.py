
import json
from websocket import create_connection
from tabulate import tabulate
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
             
        table = tabulate(df_data, headers='keys', tablefmt='github', showindex=False)
        print(table)
        print('\n')
   

def main():
    while True:
        binance_abnormal_trading()

if __name__ == "__main__":
    main()
