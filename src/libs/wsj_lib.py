import pandas as pd
import requests

def __get_market_diary():
    url = 'https://www.wsj.com/market-data/stocks/us?id=%7B%22application%22%3A%22WSJ%22%2C%22marketsDiaryType%22%3A%22overview%22%7D&type=mdc_marketsdiary'
    headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
    }
    return requests.get(url, headers=headers).json()

def get_market_breath():
    df_data = pd.DataFrame(__get_market_diary()["data"]["instrumentSets"][0]["instruments"])
    return df_data if len(df_data) >1 else pd.DataFrame()

def get_market_high_low():
    df_data = pd.DataFrame(__get_market_diary()["data"]["instrumentSets"][1]["instruments"])
    return df_data if len(df_data) >1 else pd.DataFrame()

def get_market_volume():
    df_data = pd.DataFrame(__get_market_diary()["data"]["instrumentSets"][2]["instruments"])
    return df_data if len(df_data) >1 else pd.DataFrame()

def get_market_sectors():
    url = 'https://www.wsj.com/market-data/stocks/us?id=%7B%22application%22%3A%22WSJ%22%2C%22instruments%22%3A%5B%7B%22symbol%22%3A%22INDEX%2FUS%2F%2FSPX%22%2C%22name%22%3A%22S%26P%20500%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FGSPL%22%2C%22name%22%3A%22Communication%20Services%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FGSPD%22%2C%22name%22%3A%22Consumer%20Discretionary%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FGSPS%22%2C%22name%22%3A%22Consumer%20Staples%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FGSPE%22%2C%22name%22%3A%22Energy%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FGSPF%22%2C%22name%22%3A%22Financials%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FGSPA%22%2C%22name%22%3A%22Health%20Care%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FGSPI%22%2C%22name%22%3A%22Industrials%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FGSPT%22%2C%22name%22%3A%22Information%20Technology%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FGSPM%22%2C%22name%22%3A%22Materials%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FSP500-60%22%2C%22name%22%3A%22Real%20Estate%22%7D%2C%7B%22symbol%22%3A%22INDEX%2FXX%2F%2FGSPU%22%2C%22name%22%3A%22Utilities%22%7D%5D%7D&type=mdc_quotes'
    headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
    }
    data = requests.get(url, headers=headers).json()
    df_data = pd.DataFrame(data["data"]["instruments"])
    return df_data if len(df_data) >1 else pd.DataFrame()