from src.libs import yfinance_lib
from src.libs import sqlite_lib
from src.libs import technical_indicators_lib
from src.libs import tabulate_lib
from src.libs import binance_lib
from src.libs import utils
from datetime import datetime
import pandas as pd

def process_ma_up_down(symbol, ma_period, market):
    if market == "tradfi":
        df_data = yfinance_lib.get_download_data(symbol, "1y")
    elif market == "crypto":
        df_data =binance_lib.get_quotes(symbol)
        df_data.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'close time', 'asset volume', 'number of trades', 'taker buy asset volume', 'taker buy quote volume', 'ignore']

    if len(df_data)==0 or len(df_data) < ma_period:
        return

    df_ma = technical_indicators_lib.moving_average(df_data,ma_period)

    # get db data
    search_query = f"select * from strat_moving_average where symbol ='{symbol}' and ma='{ma_period}'"
    search_data = sqlite_lib.get_record_query(search_query)

    ma = str(round(float(df_ma.iloc[0][f"MA_{ma_period}"]),3))
    last = str(round(float(df_ma.iloc[0]["close"]),3))
    signal = "Below" if ma > last else "Above"

    if len(search_data) == 0:
        insert_query = f"INSERT INTO strat_moving_average (symbol, ma, signal, updated, market) VALUES('{symbol}', '{ma_period}', '{signal}', '{datetime.now().strftime('%Y-%m-%d')}','{market}');"
        sqlite_lib.create_update_query(insert_query)
    elif search_data[0][2] != signal:
        update_query = f"UPDATE strat_moving_average SET signal='{signal}', updated='{datetime.now().strftime('%Y-%m-%d')}' WHERE symbol ='{symbol}' and ma = '{ma_period}';"
        sqlite_lib.create_update_query(update_query)

def process_ema_up_down(symbol, ma_period, market ):
    if market == "tradfi":
        df_data = yfinance_lib.get_download_data(symbol, "1y")
    elif market == "crypto":
        df_data =binance_lib.get_quotes(symbol)
        df_data.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'close time', 'asset volume', 'number of trades', 'taker buy asset volume', 'taker buy quote volume', 'ignore']
    
    if len(df_data)==0 or len(df_data) < ma_period:
        return
    
    df_ema = technical_indicators_lib.exponential_moving_average(df_data, 200)
    ema = str(round(float(df_ema.iloc[0]["EMA_200"]),3))
    last = str(round(float(df_ema.iloc[0]["close"]),3))

    signal = "Below" if ema > last else "Above"
   
    # get db data
    search_query = f"select * from strat_exponential_moving_average where symbol ='{symbol}' and ema='{ma_period}'"
    search_data = sqlite_lib.get_record_query(search_query)

    if len(search_data) == 0:
        insert_query = f"INSERT INTO strat_exponential_moving_average (symbol, ema, signal, updated, market) VALUES('{symbol}', '{ma_period}', '{signal}', '{datetime.now().strftime('%Y-%m-%d')}','{market}');"
        sqlite_lib.create_update_query(insert_query)
    elif search_data[0][2] != signal:
        update_query = f"UPDATE strat_exponential_moving_average SET signal='{signal}', updated='{datetime.now().strftime('%Y-%m-%d')}' WHERE symbol ='{symbol}' and ema = '{ma_period}';"
        sqlite_lib.create_update_query(update_query)



def report_ma(ma, market):
    search_query = f"select * from  strat_moving_average where ma='{ma}' and market = '{market}' and updated= '{datetime.now().strftime('%Y-%m-%d')}'"
    search_data = sqlite_lib.get_record_query(search_query)
    tabulate_lib.tabulate_it(f"Updated MA {ma}", pd.DataFrame(search_data, columns=['symbol', 'ma','signal','updated', 'market']))


def report_ema(ema, market):
    search_query = f"select * from  strat_exponential_moving_average where ema='{ema}' and market = '{market}' and updated= '{datetime.now().strftime('%Y-%m-%d')}'"
    search_data = sqlite_lib.get_record_query(search_query)
    tabulate_lib.tabulate_it(f"Updated EMA {ema}", pd.DataFrame(search_data, columns=['symbol', 'ema','signal','updated', 'market']))

def report_volume_up_average(symbol, market, to_tail, name=""):
    if market == "tradfi":
        df_data = yfinance_lib.get_download_data(symbol, "1y")
    elif market == "crypto":
        df_data =binance_lib.get_quotes(symbol)

    df_data["volume"] = pd.to_numeric(df_data["volume"])

    last_volume = float(df_data["volume"].tail(1))
    avg_volume = float(df_data["volume"].tail(to_tail).mean())
    if last_volume>avg_volume:
        print(f"Volume bigger than average for {name} {symbol}  Actual:{utils.print_formated_numbers(round(last_volume,2))}   Avg:{utils.print_formated_numbers(round(avg_volume,2))}")

def report_rsi_oversold(symbol, market, name=""):
    if market == "tradfi":
        df_data = yfinance_lib.get_download_data(symbol, "1y")
    elif market == "crypto":
        df_data =binance_lib.get_quotes(symbol)
        
    rsi = technical_indicators_lib.rsi(df_data)
    if round(float(rsi.tail(1)),2)<=30:
        print(f"RSI for {name} {symbol} is Oversold {round(float(rsi.tail(1)),2)} !")

def report_rsi_overbought(symbol, market, name=""):
    if market == "tradfi":
        df_data = yfinance_lib.get_download_data(symbol, "1y")
    elif market == "crypto":
        df_data =binance_lib.get_quotes(symbol)
   
    rsi = technical_indicators_lib.rsi(df_data)
    if round(float(rsi.tail(1)),2)>=70:
        print(f"RSI for {name} {symbol} is Overbought {round(float(rsi.tail(1)),2)} !")
