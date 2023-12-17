import requests
import datetime
import pandas as pd

# CNN FEEDS

def get_fear_greed_index_all():
    url = 'https://production.dataviz.cnn.io/index/fearandgreed/graphdata'
    headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
    }
    return requests.get(url, headers=headers).json()


def get_fear_greed_actual():
    data = get_fear_greed_index_all()
    df_data =pd.DataFrame(data["fear_and_greed"].items()).transpose()
    df_data.columns = df_data.iloc[0]
    df_data = df_data[1:]
    return df_data if len(df_data) >= 1 else pd.DataFrame()
   

def get_fear_greed_historical():
    data = get_fear_greed_index_all()
    df_data =pd.DataFrame(data["fear_and_greed_historical"]["data"])
    df_data.columns = ['date', 'score', 'rating']
   
    # parse timestamp to str date
    df_data['date'] = pd.to_datetime(df_data['date'], unit='ms')

    for index, row in df_data.iterrows():
        df_data.at[index,'date'] = row["date"].strftime('%Y-%m-%d')

    # remove last two rows
    df_data = df_data.iloc[:-2]

    return df_data if len(df_data) > 1 else pd.DataFrame()
   
def get_us_indices_daily_status():
    url = f'https://production.dataviz.cnn.io/markets/index/DJII-USA,SP500-CME,COMP-USA,VIX-USA/{datetime.datetime.now().date()}'
    headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
    }
    return requests.get(url, headers=headers).json()
