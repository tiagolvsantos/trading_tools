from src.implementation.reports import reportpedia
from src.libs import sqlite_lib


def _run_ma_job(market):
    print(f"Running MA jobs {market}.....")
    process_ma(market, 50)
    process_ma(market, 100)
    process_ma(market, 200)


def process_ma(market, ma):
    if market == "tradefi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()

    for symbol in list_symbols:
        reportpedia.process_ma_up_down(symbol[0], ma, market)


def report_ma(ma):
    reportpedia.report_ma(ma)

def process_volume_average(market):
    if market == "tradefi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
        to_tail = 30
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()
        to_tail = 15

    for symbol in list_symbols:
        reportpedia.report_volume_up_average(symbol[0], market, to_tail)

def process_rsi_oversold():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.report_rsi_oversold(symbol[0])

def process_rsi_overbought():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.report_rsi_overbought(symbol[0])

def run_jobs():
    print("Running jobs.....")
    _run_ma_job("tradefi")
    _run_ma_job("crypto")
    print("Running jobs done!")


