import json
import pandas as pd
import requests
from io import StringIO
from src.libs import utils


def get_fx_volatility():
    try:
        data=pd.read_csv('http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/BPJYEUVIXDailyPrices.csv',skiprows=2,index_col=0,parse_dates=True)#CBOE FX Vol
        dFXvol=  pd.DataFrame(data)
        dFXvol=  dFXvol.reset_index()
        return dFXvol
    except NameError:
        return NameError

def get_market_tape_data():
    try:
        req=requests.get(url='https://markets.cboe.com/us/equities/market_share/market/csv/history/?bias=Volume&auctions=y&oddLots=y').content
        return pd.read_csv(StringIO(req.decode('utf8')))
    except NameError:
        return NameError
    
def get_skew():
    try:
        req=requests.get(url='https://cdn.cboe.com/api/global/us_indices/daily_prices/SKEW_History.csv').content 
        data= pd.read_csv(StringIO(req.decode('utf8')),skiprows=1)
        df_data=data.reset_index()
        df_data.columns = ['index', 'date', 'last']
        return df_data
    except NameError:
        return NameError

def get_all_active_options():
    url = "http://markets.cboe.com/us/options/market_statistics/most_active/data/?mkt=cone&limit=25"
    return requests.get(url).json()["categories"][0]
  
def get_index_active_options():
    url = "http://markets.cboe.com/us/options/market_statistics/most_active/data/?mkt=cone&limit=25"
    return requests.get(url).json()["categories"][1]

def get_equity_active_options():
    url = "http://markets.cboe.com/us/options/market_statistics/most_active/data/?mkt=cone&limit=25"
    return requests.get(url).json()["categories"][2]


def parse_cbe_list(list_cboe: list):
    df_data = pd.DataFrame()
    return df_data.append(list_cboe, ignore_index = True)

def get_options_ratios():
    date = utils.get_yesterdays_date("%Y-%m-%d")
    url = f"https://cdn.cboe.com/data/us/options/market_statistics/daily/{date}_daily_options"
    response = requests.get(url)
    return {} if response.status_code == 403 or len(requests.get(url).json())==0 else requests.get(url).json()