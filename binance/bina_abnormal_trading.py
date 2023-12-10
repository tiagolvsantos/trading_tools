
import json
from websocket import create_connection
from tabulate import tabulate
import pandas as pd

def recv_to_object(websocket):
    data = websocket.recv()
    return json.loads(data)

def binance_abnormal_trading():
    websocket = create_connection("wss://bstream.binance.com:9443/stream?streams=abnormaltradingnotices")
    while True:
        data = recv_to_object(websocket)
        table = tabulate(pd.DataFrame([data["data"]]), headers='keys', tablefmt='github', showindex=False)
        print(table)
        print('\n')
   

def main():
    while True:
        binance_abnormal_trading()

if __name__ == "__main__":
    main()
