from src.libs import yfinance_lib
from src.libs import sqlite_lib
from src.libs import technical_indicators_lib
from src.libs import tabulate_lib
from datetime import datetime
import pandas as pd

def process_ma_up_down(symbol, ma_period):
    df_data = yfinance_lib.get_download_data(symbol, "1y")
    df_ma = technical_indicators_lib.moving_average(df_data,ma_period)

    # get db data
    search_query = f"select * from strat_moving_average where symbol ='{symbol}' and ma='{ma_period}'"
    search_data = sqlite_lib.get_record_query(search_query)

    ma = str(round(float(df_ma.iloc[0][f"MA_{ma_period}"]),3))
    last = str(round(float(df_ma.iloc[0]["close"]),3))
    signal = "Below" if ma > last else "Above"

    if len(search_data) == 0:
        insert_query = f"INSERT INTO strat_moving_average (symbol, ma, signal, updated) VALUES('{symbol}', '{ma_period}', '{signal}', '{datetime.now().strftime('%Y-%m-%d')}');"
        sqlite_lib.create_update_query(insert_query)
    elif search_data[0][2] != signal:
        update_query = f"UPDATE strat_moving_average SET signal='{signal}', updated='{datetime.now().strftime('%Y-%m-%d')}' WHERE symbol ='{symbol}' and ma = '{ma_period}';"
        sqlite_lib.create_update_query(update_query)


def report_ma(ma):
    search_query = f"select * from  strat_moving_average where ma='{ma}' and updated= '{datetime.now().strftime('%Y-%m-%d')}'"
    search_data = sqlite_lib.get_record_query(search_query)
    tabulate_lib.tabulate_it(f"Updated MA {ma}", pd.DataFrame(search_data, columns=['symbol', 'ma','signal','updated']))

def report_volume_up_average(symbol):
    df_data = yfinance_lib.get_download_data(symbol, "1y")
    last_volume = float(df_data["volume"].tail(1))
    avg_volume = float(df_data["volume"].tail(30).mean())
    if last_volume>avg_volume:
        print(f"Volume bigger than average for {symbol}  {round(last_volume,2)} > {round(avg_volume,2)}")

def report_rsi_oversold(symbol):
    df_data = yfinance_lib.get_download_data(symbol, "1y")
    rsi = technical_indicators_lib.rsi(df_data)
    if round(float(rsi.tail(1)),2)<=30:
        print(f"RSI for {symbol} is Oversold!")

def report_rsi_overbought(symbol):
    df_data = yfinance_lib.get_download_data(symbol, "1y")
    rsi = technical_indicators_lib.rsi(df_data)
    if round(float(rsi.tail(1)),2)>=70:
        print(f"RSI for {symbol} is Overbought!")