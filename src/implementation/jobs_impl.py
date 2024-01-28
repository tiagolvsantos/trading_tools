from src.implementation.jobs import jobpedia
from src.libs import sqlite_lib


def _run_jobs(market):
    print(f"Running MA jobs {market}.....")
    process_ma(market, 50)
    process_ma(market, 100)
    process_ma(market, 200)
    print(f"Running EMA jobs {market}.....")
    process_ema(market, 200)

def _run_jobs_data():
    process_flows()

def process_ma(market, ma):
    if market == "tradfi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()

    for symbol in list_symbols:
        jobpedia.process_ma_up_down(symbol[0], ma, market)

def process_ema(market, ema):
    if market == "tradfi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()
    for symbol in list_symbols:
        jobpedia.process_ema_up_down(symbol[0], ema, market)

def process_flows():
    list_symbols = sqlite_lib.get_stock_symbols_list()

    for symbol in list_symbols:
        if "." in symbol[0]:
            continue
        jobpedia.process_flows(symbol[0])
    jobpedia.remove_todays_flows_records()

def run_jobs():
    print("Running jobs.....")
    _run_jobs("tradfi")
    _run_jobs("crypto")
    _run_jobs_data()
    print("Running jobs done!")