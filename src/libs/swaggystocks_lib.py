import pandas as pd

def get_wsb_buzz_stocks():
    url = "https://api.beta.swaggystocks.com/wsb/sentiment/rating?timeframe=12+hours"
    try:
        return  pd.read_json(url)
    except Exception:
        return pd.DataFrame()
    