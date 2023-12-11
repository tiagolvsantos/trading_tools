import yfinance as yf
import pandas as pd
import src.libs.utils as utils

def get_options_chain(symbol, period):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.option_chain(ticker.options[period])
    except NameError:
        return NameError

def get_options_chain_expirations(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.options
    except NameError:
        return NameError

def get_call_options(symbol, period):
    try:
        ticker = yf.Ticker(symbol)
        #Expiration periods
        option_chain = ticker.option_chain(ticker.options[period])
        return option_chain[0]
    except NameError:
        return NameError    

def get_put_options(symbol, period):
    try:
        ticker = yf.Ticker(symbol)
        #Expiration periods
        option_chain = ticker.option_chain(ticker.options[period])
        return option_chain[1]
    except NameError:
        return NameError 

def get_all_option_chain_consolidated_calls(symbol):
    lst_expirations = get_options_chain_expirations(symbol)
    df_full_calls = pd.DataFrame()
    for idx, expiration in enumerate(lst_expirations):
        df_calls  = get_call_options(symbol, idx)
        df_full_calls = pd.concat([df_full_calls,df_calls])

    df_full_calls["$ Dollars traded"] = df_full_calls["lastPrice"] * df_full_calls["volume"]
    # drop nan
    df_full_calls = df_full_calls.dropna()
    # convert to float
    df_full_calls["$ Dollars traded"] = pd.to_numeric(df_full_calls["$ Dollars traded"])
    df_full_calls["strike"] = pd.to_numeric(df_full_calls["strike"])

    df_arranged_calls =  pd.DataFrame(columns=['Strike','$ Dollars Traded'])

    for indx,row in df_full_calls.iterrows():
        if row['strike'] in df_arranged_calls['Strike'].values: 
            df_arranged_calls.loc[df_arranged_calls['Strike'] == row['strike']]["$ Dollars Traded"] = df_arranged_calls.loc[df_arranged_calls['Strike'] == row['strike']]["$ Dollars Traded"] + row['volume'] *  row['strike']
        else:
            new_row= pd.DataFrame (
                {   "Strike": [row['strike']],
                    "$ Dollars Traded": [row['volume'] *  row['strike']]
                })
            df_arranged_calls = pd.concat([df_arranged_calls,new_row])

    for index, row in df_arranged_calls.iterrows():
        row['$ Dollars Traded'] = utils.print_formated_numbers(int(round(float(row['$ Dollars Traded']),0)))

    return df_arranged_calls.sort_values(['$ Dollars Traded'], ascending=False).groupby('$ Dollars Traded').head(5)


def get_put_options_itm(symbol, period):
    try:
        ticker = yf.Ticker(symbol)

        option_chain = ticker.option_chain(ticker.options[period])
        option_puts = option_chain[1]

        return option_puts.loc[option_puts['inTheMoney'] == True]
    except NameError:
        return NameError   

def get_call_options_itm(symbol, period):
    try:
        ticker = yf.Ticker(symbol)

        option_chain = ticker.option_chain(ticker.options[period])
        option_calls = option_chain[0]

        return option_calls.loc[option_calls['inTheMoney'] == True]
    except NameError:
        return NameError  

def get_symbol_last_quote(symbol):
    try:
        ticker = yf.Ticker(symbol)
        historical_price = ticker.history()
        last_price=(historical_price.tail(1)["Close"]).tolist()
        return (str(last_price).replace("[","")).replace("]","")
    except NameError:
        return NameError
    
def get_etf_nav(symbol):
    try:
        ticker = yf.Ticker(symbol)
        symbol_info = ticker.get_info()

        if "navPrice" in symbol_info:
            return 0 if symbol_info["navPrice"] is None else symbol_info["navPrice"]
        return 0


    except NameError:
        return NameError

def get_symbol_name(symbol):
    try:
        ticker = yf.Ticker(symbol)
        symbol_info=ticker.get_info()
        return str(symbol_info["longName"])
    except NameError:
        return NameError
    
def get_symbol_historical_data(symbol: str, interval ="1d"):
    try:
        ticker = yf.Ticker(symbol)
        df_data =  ticker.history("max",interval)
        
        if len(df_data) >0:
            df_data.reset_index(level=0, inplace=True)
            df_data["Date"] = df_data["Date"].dt.tz_localize(None)

        if len(df_data.columns) == 8:
            df_data.columns = ['date', 'open', 'high', 'low','close','volume','dividends','stock split']
            return df_data
        elif len(df_data.columns) == 9:
            df_data.columns = ['date', 'open', 'high', 'low','close','volume','dividends','stock split', 'capital gains'] 
            return df_data
        
        else:
            return pd.DataFrame()
    except NameError:
        return NameError

def get_symbol_historical_data_from(symbol,since_date, interval ="1d"):
    try:
        ticker = yf.Ticker(symbol)
        df_data =  ticker.history( start=since_date,interval=interval)

        if len(df_data) >0:
            df_data.reset_index(level=0, inplace=True)
            df_data["Date"] = df_data["Date"].dt.tz_localize(None)

        if len(df_data.columns) == 8:
            df_data.columns = ['date', 'open', 'high', 'low','close','volume','dividends','stock split']
            return df_data
        elif len(df_data.columns) == 9:
            df_data.columns = ['date', 'open', 'high', 'low','close','volume','dividends','stock split', 'capital gains'] 
            return df_data
        
        else:
           return pd.DataFrame()
    except NameError:
        return NameError

# period  1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
def get_download_data(symbol,period = "ytd", interval ="1d"):
    try:
        df_data = (yf.download(tickers=symbol,period=period,interval=interval,progress=False).dropna())
        df_data.reset_index(level=0, inplace=True)
        df_data["Date"] = df_data["Date"].dt.tz_localize(None)
        if len(df_data.columns) > 0 and len(df_data.columns) == 7:
            df_data.columns = ['date', 'open', 'high', 'low','close','adj close','volume']
            return df_data
        elif  len(df_data.columns) > 0 and len(df_data.columns) == 9:
            df_data.columns = ['date', 'open', 'high', 'low','close','volume','dividends','stock split', 'capital gains'] 
            return df_data
        else:
            pd.DataFrame()
    except NameError:
        return NameError

def get_asset_returns_from_date(symbol, from_date): # 2023-01-01 
    df_data = get_symbol_historical_data_from(symbol,from_date)
    if len(df_data) >0:
        return round(float(pd.DataFrame((df_data['close'].pct_change(1).dropna().to_numpy())).sum())*100, 3)
    else:
        return 0