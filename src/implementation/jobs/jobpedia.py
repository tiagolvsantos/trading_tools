from src.libs import webull_lib
from src.libs import yfinance_lib
from src.libs import sqlite_lib
from src.libs import technical_indicators_lib
from src.libs import binance_lib
from src.libs import utils
import pandas as pd
from datetime import datetime


def process_flows(symbol: str):
    counter = 0

    try:
        inflow_data = webull_lib.get_capital_flow(symbol)
    except Exception:
        print(f"ERROR GETTING DATA FOR {symbol}")
        return

    if inflow_data["currencyId"] == 0:
        print(f"Skip no data for {symbol}")
        return
    
    df_inflow_data = pd.json_normalize(inflow_data['historical'])
    df_inflow_data['date'] = pd.to_datetime(df_inflow_data['date'])
    # get data from bd 
    query_last_record = f"select * from data_stock_flows where symbol='{symbol}' order by date desc limit 1"
    bd_last_record = sqlite_lib.get_record_query(query_last_record)

    if len(bd_last_record) == 0:
        print(f"New data for flows - insert {symbol}")
        for index, row in df_inflow_data.iterrows():
            print(row['date'])
            query_insert = f"INSERT INTO data_stock_flows(`date`, symbol, superLargeInflow, superLargeOutflow, superLargeNetFlow, largeInflow, largeOutflow, largeNetFlow, newLargeInflow, newLargeOutflow, newLargeNetFlow, newLargeInflowRatio, newLargeOutflowRatio, mediumInflow, mediumOutflow, mediumNetFlow, mediumInflowRatio, mediumOutflowRatio, smallInflow, smallOutflow, smallNetFlow, smallInflowRatio, smallOutflowRatio, majorInflow, majorInflowRatio, majorOutflow, majorOutflowRatio, majorNetFlow, retailInflow, retailInflowRatio, retailOutflow, retailOutflowRatio)VALUES('{row['date']}', '{symbol}', '{row['item.superLargeInflow']}', '{row['item.superLargeOutflow']}', '{row['item.superLargeNetFlow']}', '{row['item.largeInflow']}', '{row['item.largeOutflow']}', '{row['item.largeNetFlow']}', '{row['item.newLargeInflow']}', '{row['item.newLargeOutflow']}', '{row['item.newLargeNetFlow']}', '{row['item.newLargeInflowRatio']}', '{row['item.newLargeOutflowRatio']}', '{row['item.mediumInflow']}', '{row['item.mediumOutflow']}', '{row['item.mediumNetFlow']}', '{row['item.mediumInflowRatio']}', '{row['item.mediumOutflowRatio']}', '{row['item.smallInflow']}', '{row['item.smallOutflow']}', '{row['item.smallNetFlow']}', '{row['item.smallInflowRatio']}', '{row['item.smallOutflowRatio']}', '{row['item.majorInflow']}', '{row['item.majorInflowRatio']}', '{row['item.majorOutflow']}', '{row['item.majorOutflowRatio']}', '{row['item.majorNetFlow']}', '{row['item.retailInflow']}', '{row['item.retailInflowRatio']}', '{row['item.retailOutflow']}', '{row['item.retailOutflowRatio']}');"
            sqlite_lib.create_update_query(query_insert)

    elif len(bd_last_record) > 0:
        df_inflow_data = df_inflow_data[df_inflow_data["date"] > bd_last_record[0][0]]
        print(f"Last flows data for {symbol} is {bd_last_record[0][0]}")
        for index, row in df_inflow_data.iterrows():
            query_insert = f"INSERT INTO data_stock_flows(`date`, symbol, superLargeInflow, superLargeOutflow, superLargeNetFlow, largeInflow, largeOutflow, largeNetFlow, newLargeInflow, newLargeOutflow, newLargeNetFlow, newLargeInflowRatio, newLargeOutflowRatio, mediumInflow, mediumOutflow, mediumNetFlow, mediumInflowRatio, mediumOutflowRatio, smallInflow, smallOutflow, smallNetFlow, smallInflowRatio, smallOutflowRatio, majorInflow, majorInflowRatio, majorOutflow, majorOutflowRatio, majorNetFlow, retailInflow, retailInflowRatio, retailOutflow, retailOutflowRatio)VALUES('{row['date']}', '{symbol}', '{row['item.superLargeInflow']}', '{row['item.superLargeOutflow']}', '{row['item.superLargeNetFlow']}', '{row['item.largeInflow']}', '{row['item.largeOutflow']}', '{row['item.largeNetFlow']}', '{row['item.newLargeInflow']}', '{row['item.newLargeOutflow']}', '{row['item.newLargeNetFlow']}', '{row['item.newLargeInflowRatio']}', '{row['item.newLargeOutflowRatio']}', '{row['item.mediumInflow']}', '{row['item.mediumOutflow']}', '{row['item.mediumNetFlow']}', '{row['item.mediumInflowRatio']}', '{row['item.mediumOutflowRatio']}', '{row['item.smallInflow']}', '{row['item.smallOutflow']}', '{row['item.smallNetFlow']}', '{row['item.smallInflowRatio']}', '{row['item.smallOutflowRatio']}', '{row['item.majorInflow']}', '{row['item.majorInflowRatio']}', '{row['item.majorOutflow']}', '{row['item.majorOutflowRatio']}', '{row['item.majorNetFlow']}', '{row['item.retailInflow']}', '{row['item.retailInflowRatio']}', '{row['item.retailOutflow']}', '{row['item.retailOutflowRatio']}');"
            sqlite_lib.create_update_query(query_insert)

def remove_todays_flows_records():
    query_delete_nok_record = f"delete from data_stock_flows where date='{utils.get_todays_date('%Y-%m-%d')} 00:00:00'"
    sqlite_lib.create_update_query(query_delete_nok_record)

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
        print(f"Insert {symbol} for {ma_period} MA strategy")
        insert_query = f"INSERT INTO strat_moving_average (symbol, ma, signal, updated, market) VALUES('{symbol}', '{ma_period}', '{signal}', '{datetime.now().strftime('%Y-%m-%d')}','{market}');"
        sqlite_lib.create_update_query(insert_query)
    elif search_data[0][2] != signal:
        print(f"Update {symbol} for {ma_period} MA strategy")
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
        print(f"Insert {symbol} for {ma_period} EMA strategy")
        insert_query = f"INSERT INTO strat_exponential_moving_average (symbol, ema, signal, updated, market) VALUES('{symbol}', '{ma_period}', '{signal}', '{datetime.now().strftime('%Y-%m-%d')}','{market}');"
        sqlite_lib.create_update_query(insert_query)
    elif search_data[0][2] != signal:
        print(f"Update {symbol} for {ma_period} EMA strategy")
        update_query = f"UPDATE strat_exponential_moving_average SET signal='{signal}', updated='{datetime.now().strftime('%Y-%m-%d')}' WHERE symbol ='{symbol}' and ema = '{ma_period}';"
        sqlite_lib.create_update_query(update_query)

def process_market_breath(period, indx):
    query_below=f"select count(signal) from strat_moving_average  where signal ='Below' and ma ='{period}' and symbol in (select symbol from data_index_constituints where indx='{indx}' )"
    query_above=f"select count(signal) from strat_moving_average  where signal ='Above' and ma ='{period}' and symbol in (select symbol from data_index_constituints where indx='{indx}' )"
    data_above = sqlite_lib.get_record_query(query_above)[0][0]
    data_below = sqlite_lib.get_record_query(query_below)[0][0]

    insert_query = f"INSERT INTO data_market_breath(date, period, above, below, indx)VALUES('{utils.get_yesterdays_date('%Y-%m-%d')}', '{period}', '{data_above}', '{data_below}', '{indx}');"
    sqlite_lib.create_update_query(insert_query)

def process_momentum(market:str, to_measure:int):
    if market == "tradfi":
        df_symbols = sqlite_lib.get_stock_symbols_list()
    elif market == "crypto":
        df_symbols = sqlite_lib.get_crypto_symbols_list()

    df_momentum=pd.DataFrame(columns = [
        "symbol",   
        "trend",
        "momentum_value",
        "period",
        "region"
        ])

    for symbol in df_symbols:
        print(symbol[0])
        if market == "tradfi":
            df_data = yfinance_lib.get_download_data(symbol[0], "1y")
        elif market == "crypto":
            df_data =binance_lib.get_quotes(symbol[0])

        if len(df_data)==0:
            continue
        if round(float(df_data['close'].head(1)),2) <= 0.1:
            continue
        last_price = round(float(df_data['close'].head(1)),2)
        to_measure_days_price = round(float((df_data['close'].head(20)).tail(1)),2)

        momentum = round((last_price / to_measure_days_price) * 100, 3)
        momentum_text = "Bull" if momentum >= 100 else "Bear"

        newRow= pd.DataFrame (
            {   "symbol": symbol[0], 
                "trend": momentum_text,
                "momentum_value":momentum,
                "period": f"{to_measure} days",
                "region": symbol[2]
            }, index=[0])
        df_momentum = pd.concat([df_momentum,newRow])
        insert_query =f"INSERT INTO data_asset_momentum (date, symbol, momentum) VALUES('{utils.get_yesterdays_date('%Y-%m-%d')}', '{symbol[0]}', '{momentum}')"
        sqlite_lib.create_update_query(insert_query)
    file_path =f"generated_reports\\{market}_momentum.xlsx"
    utils.export_excel(file_path, df_momentum)