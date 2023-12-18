import requests
import pandas as pd
from src.libs import utils 
from datetime import datetime

BINANCE_API_URL = "https://api.binance.com"
# 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
def get_quotes(symbol: str, interval="1d"):
    url = f"{BINANCE_API_URL}/api/v3/klines?symbol={symbol}&interval={interval}"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
    except Exception:
        return pd.DataFrame()
    df_quote.columns = ['open time', 'open', 'high', 'low', 'close', 'volume', 'close time', 'asset volume', 'number of trades', 'taker buy asset volume', 'taker buy quote volume', 'ignore']
    df_quote['open time'] = df_quote['open time'].astype(str)
    df_quote['close time'] = df_quote['close time'].astype(str)
    for index, row in df_quote.iterrows():
        df_quote.at[index,'open time']= str(utils.epoch_to_datetime(int(row['open time'])))
        df_quote.at[index,'close time']= str(utils.epoch_to_datetime(int(row['close time'])))
    return df_quote if len(df_quote)>0 else pd.DataFrame()

def get_open_Interest(symbol: str, interval: str):
    url = f"https://fapi.binance.com/futures/data/openInterestHist?symbol={symbol}&period={interval}&limit=500"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
    except Exception:
        return pd.DataFrame()
    if len(df_quote) > 1:
        df_quote.columns = ['symbol', 'oi', 'oi in $', 'date']
        df_quote['date'] = df_quote['date'].astype(str)
        for index, row in df_quote.iterrows():
            df_quote.at[index,'date']= str(utils.epoch_to_datetime(int(row['date'])))
    return df_quote if len(df_quote)>0 else pd.DataFrame()

def get_top_accounts_long_short_accounts(symbol: str, interval: str):
    url = f"https://fapi.binance.com/futures/data/topLongShortAccountRatio?symbol={symbol}&period={interval}"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
    except Exception:
        return pd.DataFrame()
    df_quote.columns = ['symbol', 'long', 'short', 'long/short', 'date']
    df_quote['date'] = df_quote['date'].astype(str)
    for index, row in df_quote.iterrows():
        df_quote.at[index,'date']= str(utils.epoch_to_datetime(int(row['date'])))
    return df_quote if len(df_quote)>0 else pd.DataFrame()


def get_top_accounts_long_short_positions(symbol: str, interval: str):
    url = f"https://fapi.binance.com/futures/data/topLongShortPositionRatio?symbol={symbol}&period={interval}"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
    except Exception:
        return pd.DataFrame()
    df_quote.columns = ['symbol', 'long', 'short', 'long/short', 'date']
    df_quote['date'] = df_quote['date'].astype(str)
    for index, row in df_quote.iterrows():
        df_quote.at[index,'date']= str(utils.epoch_to_datetime(int(row['date'])))
    return df_quote if len(df_quote)>0 else pd.DataFrame()

def get_global_long_short_account_ratio(symbol: str, interval: str):
    url = f"https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol={symbol}&period={interval}"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
    except Exception:
        return pd.DataFrame()
    df_quote.columns = ['symbol', 'long', 'long/short', 'short', 'date']
    df_quote['date'] = df_quote['date'].astype(str)
    for index, row in df_quote.iterrows():
        df_quote.at[index, 'date'] = str(utils.epoch_to_datetime(int(row['date'])))
    return df_quote if len(df_quote) > 0 else pd.DataFrame()


def get_taker_long_short_ratio(symbol: str, interval: str):
    url = f"https://fapi.binance.com/futures/data/takerlongshortRatio?symbol={symbol}&period={interval}"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
    except Exception:
        return pd.DataFrame()
    df_quote.columns = ['buy/sell ratio', 'sell volume', 'buy volume', 'date']
    df_quote['date'] = df_quote['date'].astype(str)
    for index, row in df_quote.iterrows():
        df_quote.at[index,'date']= str(utils.epoch_to_datetime(int(row['date'])))
    return df_quote if len(df_quote)>0 else pd.DataFrame()

# period	ENUM	YES	"5m","15m","30m","1h","2h","4h","6h","12h","1d"
def get_open_interest_statiistics(symbol: str, interval: str):
    url = f"https://fapi.binance.com/futures/data/openInterestHist?symbol={symbol}&period={interval}"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
    except Exception:
        return pd.DataFrame()
    df_quote.columns = ['symbol', 'sum OI', 'sum OI value', 'date']
    df_quote['date'] = df_quote['date'].astype(str)
    for index, row in df_quote.iterrows():
        df_quote.at[index,'date']= str(utils.epoch_to_datetime(int(row['date'])))
    return df_quote if len(df_quote)>0 else pd.DataFrame()

def get_order_book_depth(symbol:str):
    r = requests.get("https://api.binance.com/api/v3/depth?limit=5000",
                    params=dict(symbol=symbol))
    results = r.json()
    frames = {side: pd.DataFrame(data=results[side], columns=["price", "quantity"],
                                dtype=float)
            for side in ["bids", "asks"]}
    return [frames[side].assign(side=side) for side in frames]


def get_daily_aggtrades(symbol: str):
    header_list = ["id","price","qty","a","b","date","isBuyerMaker","isBestMatch"]
    try:
        df_data = pd.read_csv(f'https://data.binance.vision/data/spot/daily/aggTrades/{symbol}/{symbol}-aggTrades-{utils.get_yesterdays_date("%Y-%m-%d")}.zip',compression='zip', names=header_list)
    except Exception:
        return pd.DataFrame()
    df_data['date'] = df_data['date'].astype(str)
    for index, row in df_data.iterrows():
        df_data.at[index,'date']= str(datetime.fromtimestamp(int(row['date'])/1000))
    return df_data if len(df_data)>0 else pd.DataFrame()

def top_gainers():
    url = f"{BINANCE_API_URL}/api/v3/ticker/24hr"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
    except Exception:
        return pd.DataFrame()
    df_quote["priceChangePercent"] = pd.to_numeric(df_quote["priceChangePercent"] , downcast="float")
    return df_quote.sort_values(by="priceChangePercent", ascending=False)

def top_loosers():
    url = f"{BINANCE_API_URL}/api/v3/ticker/24hr"
    try:
        df_quote = pd.DataFrame(requests.get(url).json())
    except Exception:
        return pd.DataFrame()
    df_quote["priceChangePercent"] = pd.to_numeric(df_quote["priceChangePercent"] , downcast="float")
    return df_quote.sort_values(by="priceChangePercent", ascending=True)
