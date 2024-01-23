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

def report_bb_bands_outside(symbol, market, name=""):
    if market == "tradfi":
        df_data = yfinance_lib.get_download_data(symbol, "1y")
    elif market == "crypto":
        df_data =binance_lib.get_quotes(symbol)
        df_data.rename(columns={"open time": "date"})
        df_data["close"] = pd.to_numeric(df_data["close"])
        df_data["volume"] = pd.to_numeric(df_data["volume"])
   
    if len(df_data) <0:
        return pd.DataFrame()
    
    df_bb = technical_indicators_lib.bollinger_bands(df_data)
    avg_volume = round(df_bb["volume"].mean(),2)

    if float(df_bb.tail(1)["close"]) > float(df_bb.tail(1)["UpperBand"]) and float(df_bb.tail(1)["volume"]) > avg_volume:
        tabulate_lib.print_it_line_red(f"Price for {symbol} is above Upper Bollinger Band.")
    if float(df_bb.tail(1)["close"]) < float(df_bb.tail(1)["LowerBand"]) and float(df_bb.tail(1)["volume"]) > avg_volume:
        tabulate_lib.print_it_line_green(f"Price for {symbol} is below Lower Bollinger Band.")

def report_momentum(market:str, to_measure:int):
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
        if market == "tradfi":
            df_data = yfinance_lib.get_download_data(symbol[0], "1y")
        elif market == "crypto":
            df_data =binance_lib.get_quotes(symbol[0])


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

    file_path =f"generated_reports\\{market}_momentum.xlsx"
    utils.export_excel(file_path, df_momentum)

def report_candles(market:str):
    if market == "tradfi":
        df_symbols = sqlite_lib.get_stock_symbols_list()
    elif market == "crypto":
        df_symbols = sqlite_lib.get_crypto_symbols_list()

    df_candles=pd.DataFrame(columns = [
        "symbol",   
        "Bullish swing",
        "Bearish swing",
        "Bearish pinbar",
        "Inside bar",
        "Outside bar",  
        "Bullish engulfing",
        "Bearish engulfing" 
        ])


    for symbol in df_symbols:

        if market == "tradfi":
            df_data = yfinance_lib.get_download_data(symbol[0], "1mo")
        elif market == "crypto":
            df_data =binance_lib.get_quotes(symbol[0])

        # Parse data columns
        df_data["open"] = pd.to_numeric(df_data["open"])
        df_data["close"] = pd.to_numeric(df_data["close"])
        df_data["low"] = pd.to_numeric(df_data["low"])
        df_data["high"] = pd.to_numeric(df_data["high"])

        # Compute Strategy
        for i in range(2,df_data.shape[0]):
            current = df_data.iloc[i,:]
            prev = df_data.iloc[i-1,:]
            prev_2 = df_data.iloc[i-2,:]
            realbody = abs(current['open'] - current['close'])
            candle_range = current['high'] - current['low']
            idx = df_data.index[i]

            ## Bulllish Swing
            df_data.loc[idx,'Bullish swing'] = current['low'] > prev['low'] and prev['low'] < prev_2['low']

            ## Bearish Swing
            df_data.loc[idx,'Bearish swing'] = current['high'] < prev['high'] and prev['high'] > prev_2['high']

            ## Bearish pinbar
            df_data.loc[idx,'Bearish pinbar'] = realbody <= candle_range/3 and max(current['open'] , current['close']) < (current['low'] + current['low'])/2 and current['high'] > prev['high']

            ## Inside bar
            df_data.loc[idx,'Inside bar'] = current['high'] < prev['high'] and current['low'] > prev['low']

            ## Outside bar
            df_data.loc[idx,'Outside bar'] = current['high'] > prev['high'] and current['low'] < prev['low']

            ## Bullish engulfing
            df_data.loc[idx,'Bullish engulfing'] = current['high'] > prev['high'] and current['low'] < prev['low'] and realbody >= 0.8 * candle_range and current['close'] > current['open']

            ## Bearish engulfing
            df_data.loc[idx,'Bearish engulfing'] = current['high'] > prev['high'] and current['low'] < prev['low'] and realbody >= 0.8 * candle_range and current['close'] < current['open']

            df_data.fillna(False, inplace=True)

        newRow= pd.DataFrame (
            {  
                "symbol": symbol[0],   
                "Bullish swing": str(df_data.tail(1)["Bullish swing"].bool()),
                "Bearish swing": str(df_data.tail(1)["Bearish swing"].bool()),
                "Bearish pinbar": str(df_data.tail(1)["Bearish pinbar"].bool()),
                "Inside bar": str(df_data.tail(1)["Inside bar"].bool()),
                "Outside bar": str(df_data.tail(1)["Outside bar"].bool()),  
                "Bullish engulfing": str(df_data.tail(1)["Bullish engulfing"].bool()),
                "Bearish engulfing": str(df_data.tail(1)["Bearish engulfing"].bool()) 
            }, index=[0])
        df_candles = pd.concat([df_candles,newRow])
    file_path =f"generated_reports\\{market}_candles.xlsx"
    utils.export_excel(file_path, df_candles)


def report_harmonics(market:str):
    if market == "tradfi":
        df_symbols = sqlite_lib.get_stock_symbols_list()
    elif market == "crypto":
        df_symbols = sqlite_lib.get_crypto_symbols_list()

    for symbol in df_symbols:
        if market == "tradfi":
            df_data = yfinance_lib.get_download_data(symbol[0], "2y")
        elif market == "crypto":
            df_data =binance_lib.get_quotes(symbol[0])

        a = technical_indicators_lib.harmonics(df_data, symbol)




