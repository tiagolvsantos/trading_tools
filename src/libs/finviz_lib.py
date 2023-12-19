import pandas as pd
from finvizfinance.quote import finvizfinance
from finvizfinance.screener.overview import Overview
from finvizfinance.screener.ownership import Ownership
from finvizfinance.screener.technical import Technical


def symbol_fundamentals(symbol:str):
    if symbol:
        stock = finvizfinance(symbol)
        return stock.ticker_fundament()
    return 



def symbol_description(symbol:str):
    if symbol:
        stock = finvizfinance(symbol)
        return stock.ticker_description()
    return 

def symbol_fullinfo(symbol:str):
    if symbol:
        stock = finvizfinance(symbol)
        return stock.ticker_full_info()
    return 

def symbol_news(symbol:str):
    if symbol:
        stock = finvizfinance(symbol)
        return stock.ticker_news()
    return 

def symbol_insider_trading(symbol:str):
    if symbol:
        stock = finvizfinance(symbol)
        return stock.ticker_inside_trader()
    return pd.DataFrame()


def get_technicals():
    technicals = Technical()
    filters_dict = {'Exchange':'Any','Index':'S&P 500'}
    technicals.set_filter(filters_dict=filters_dict)
    df_data = technicals.screener_view()
    return df_data if len(df_data) >0 else pd.DataFrame()

def get_overiew():
    overview = Overview()
    filters_dict = {'Exchange':'Any','Index':'S&P 500'}
    overview.set_filter(filters_dict=filters_dict)
    df_data = overview.screener_view()
    return df_data if len(df_data) >0 else pd.DataFrame()