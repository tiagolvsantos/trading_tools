import pandas as pd
import requests
from io import StringIO
import warnings
warnings.filterwarnings("ignore")

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
        req=requests.get(url='https://www.cboe.com/publish/scheduledtask/mktdata/datahouse/skewdailyprices.csv').content 
        data= pd.read_csv(StringIO(req.decode('utf8')),skiprows=1)
        data=data.reset_index()
        return data
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