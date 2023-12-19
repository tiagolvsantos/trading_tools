from src.implementation.reports import reportpedia
from src.libs import sqlite_lib


def _run_jobs(market):
    print(f"Running MA jobs {market}.....")
    process_ma(market, 50)
    process_ma(market, 100)
    process_ma(market, 200)
    print(f"Running EMA jobs {market}.....")
    process_ema(market, 200)


def process_ma(market, ma):
    if market == "tradefi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()

    for symbol in list_symbols:
        reportpedia.process_ma_up_down(symbol[0], ma, market)

def process_ema(market, ema):
    if market == "tradefi":
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
    if market == "tradefi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
        to_tail = 30
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()
        to_tail = 30

    for symbol in list_symbols:
        reportpedia.report_volume_up_average(symbol[0], market, to_tail)

def process_rsi_oversold():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.report_rsi_oversold(symbol[0],"tradefi")

def process_rsi_overbought():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.report_rsi_overbought(symbol[0],"tradefi")

def run_jobs():
    print("Running jobs.....")
    _run_jobs("tradefi")
    _run_jobs("crypto")
    print("Running jobs done!")


