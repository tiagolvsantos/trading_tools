from src.libs import yfinance_lib
from src.libs import sqlite_lib
from src.libs import technical_indicators_lib
from datetime import datetime

def report_ma_up_down(symbol, ma_period):
    df_data = yfinance_lib.get_download_data(symbol, "1y")
    df_ma = technical_indicators_lib.moving_average(df_data,50)

    # get db data
    search_query = f"select * from strat_moving_average where symbol ='{symbol}' and ma='{ma_period}'"
    search_data = sqlite_lib.get_record_query(search_query)

    ma = str(round(float(df_ma.iloc[0][f"MA_{ma_period}"]),3))
    last = str(round(float(df_ma.iloc[0]["close"]),3))
    signal = "Below" if ma > last else "Above"

    if len(search_data) == 0:
        insert_query = f"INSERT INTO strat_moving_average (symbol, ma, signal, updated) VALUES('{symbol}', '{ma_period}', '{signal}', '{datetime.now().strftime('%Y-%m-%d')}');"
        sqlite_lib.create_update_query(insert_query)
    else:
        update_query = f"UPDATE strat_moving_average SET signal='{signal}', updated='{datetime.now().strftime('%Y-%m-%d')}' WHERE symbol ='{symbol}' and ma = '{ma_period}';"
        sqlite_lib.create_update_query(update_query)




