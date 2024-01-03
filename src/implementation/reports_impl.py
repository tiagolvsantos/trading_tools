from src.implementation.reports import reportpedia
from src.implementation.charts import chartpedia
from src.libs import sqlite_lib


def _run_jobs(market):
    print(f"Running MA jobs {market}.....")
    process_ma(market, 50)
    process_ma(market, 100)
    process_ma(market, 200)
    print(f"Running EMA jobs {market}.....")
    process_ema(market, 200)


def process_ma(market, ma):
    if market == "tradfi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()

    for symbol in list_symbols:
        reportpedia.process_ma_up_down(symbol[0], ma, market)

def process_ema(market, ema):
    if market == "tradfi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()
    for symbol in list_symbols:
        reportpedia.process_ema_up_down(symbol[0], ema, market)


def report_ma(ma, market):
    reportpedia.report_ma(ma, market)

def report_ema(ma, market):
    reportpedia.report_ema(ma, market)

def process_volume_average(market):
    if market == "tradfi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
        to_tail = 30
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()
        to_tail = 15

    for symbol in list_symbols:
        reportpedia.report_volume_up_average(symbol[0], market, to_tail, symbol[1])

def process_rsi_oversold():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.report_rsi_oversold(symbol[0],"tradfi", symbol[1])

def process_rsi_overbought():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.report_rsi_overbought(symbol[0],"tradfi", symbol[1])

def run_jobs():
    print("Running jobs.....")
    _run_jobs("tradfi")
    _run_jobs("crypto")
    print("Running jobs done!")

def process_cot_reports():
    list_commodities= {'WTI': 'CFTC/06742U_FO_ALL', 
                       'GOLD': 'CFTC/088691_FO_ALL', 
                       'NATGAS': 'CFTC/0233AT_FO_ALL', 
                       'COPPER': 'CFTC/085692_FO_ALL', 
                       'RBOB': 'CFTC/111659_FO_ALL', 
                       'SILVER': 'CFTC/084691_FO_ALL', 
                       'CORN': 'CFTC/002602_FO_ALL', 
                       'SOYBEANS': 'CFTC/005602_FO_ALL', 
                       'WHEAT': 'CFTC/001612_FO_ALL'}
    chartpedia.plot_cot_report(list_commodities)

    list_indices= { 'BTC': 'CFTC/133741_F_ALL', 
                    'SPX': 'CFTC/13874P_FO_ALL', 
                    'NASDAQ100': 'CFTC/20974P_FO_ALL', 
                    'RUSSELL2000': 'CFTC/239742_FO_ALL', 
                    'VIX': 'CFTC/1170E1_FO_ALL', 
                    'USD': 'CFTC/098662_FO_ALL', 
                    'EUR': 'CFTC/099741_FO_ALL', 
                    'YEN': 'CFTC/097741_FO_ALL', 
                    'GBP': 'CFTC/096742_FO_ALL'}
    chartpedia.plot_cot_report(list_indices)

