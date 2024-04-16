from src.implementation.jobs import jobpedia
from src.libs import sqlite_lib


def _run_jobs(market, run_emas=False):
    print(f"Running MA jobs {market}.....")
    process_ma(market, 50)
    process_ma(market, 100)
    process_ma(market, 200)
    if run_emas:
        print(f"Running EMA jobs {market}.....")
        process_ema(market, 200)


def _run_jobs_data(run_momentum_reports=False):
    process_flows()
    process_market_breath_tradfi()
    process_market_breath_crypto()
    if run_momentum_reports:
        process_momentum("tradfi",10)
        process_momentum("crypto",10)

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

def process_market_breath_tradfi():
    jobpedia.process_market_breath("50","sp500")
    jobpedia.process_market_breath("100","sp500")
    jobpedia.process_market_breath("200","sp500")

    jobpedia.process_market_breath("50","nasdaq100")
    jobpedia.process_market_breath("100","nasdaq100")
    jobpedia.process_market_breath("200","nasdaq100")

def process_market_breath_crypto():
    jobpedia.process_market_breath("50","hash11")
    jobpedia.process_market_breath("100","hash11")
    jobpedia.process_market_breath("200","hash11")

    jobpedia.process_market_breath("50","coindex21")
    jobpedia.process_market_breath("100","coindex21")
    jobpedia.process_market_breath("200","coindex21")

def process_momentum(market, to_measure):
    print(f"Running momentum report for {market} ....")
    jobpedia.process_momentum(market, to_measure)

    
def run_jobs():
    print("Running jobs.....")
    _run_jobs("tradfi")
    _run_jobs("crypto")
    _run_jobs_data()
    print("Running jobs done!")