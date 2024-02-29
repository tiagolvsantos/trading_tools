from src.libs import tabulate_lib

import json
from websocket import create_connection
import pandas as pd
import time
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' #  To hide pygame’s console window
import pygame.mixer


def recv_to_object(websocket):
    data = websocket.recv()
    return json.loads(data)

def epoch_to_datetime(epoch_date: int):
    if len(str(epoch_date)) > 10:
        epoch_date = str(epoch_date)[:-3]
    timeArray = time.localtime(int(epoch_date))
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

def binance_abnormal_trading():
    list_watch_symbols=['BTCUSDT', 'ETHUSDT', 'SOLUSDT','BNBUSDT', 'ADAUSDT','AVAUSDT','AVAXUSDT',
                        'XRPUSDT','LINKUSDT','DOTUSDT','MATICUSDT','UNIUSDT','LTCUSDT','APTUSDT',
                        'ETCUSDT','NEARUSDT','FILUSDT','INJUSDT','OPUSDT','VETUSDT','LDOUSDT','TIAUSDT',
                        'CROUSDT','SEIUSDT','ARBUSDT','ORDIUSDT','ELGDUSDT','FTMUSDT','PEPEUSDT','APEUSDT']
    pygame.mixer.init()
    websocket = create_connection("wss://bstream.binance.com:9443/stream?streams=abnormaltradingnotices")
    while True:
        data = recv_to_object(websocket)
       
        df_data = pd.DataFrame([data["data"]])

        for index, row in df_data.iterrows():
            if df_data.at[index,'symbol'] in list_watch_symbols:
                df_data.at[index,'sendTimestamp']= str(epoch_to_datetime(int(row['sendTimestamp'])))
                df_data.at[index,'priceChange']= f"{(round(float(row['priceChange']),2)*100)}%"
                if df_data.at[index,'period'] == "MINUTE_5":
                    # Load your song file
                    pygame.mixer.music.load('assets\level-complete-mobile-game-app-locran-1-00-06.mp3')
                    pygame.mixer.music.play()
                tabulate_lib.tabulate_it("",df_data)
                print('\n')
   

def main():
    while True:
        binance_abnormal_trading()