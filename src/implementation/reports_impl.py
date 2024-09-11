from src.implementation.reports import reportpedia
from src.implementation.reports import sp500_reports
from src.implementation.charts import chartpedia
from src.libs import sqlite_lib
from src.libs import tabulate_lib



def report_ma(ma, market):
    reportpedia.report_ma(ma, market)

def report_ema(ma, market):
    reportpedia.report_ema(ma, market)

def process_volume_average(market):
    if market == "tradfi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
        to_tail = 15
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()
        to_tail = 15

    above_avg_counter = 0
    for symbol in list_symbols:
        result = reportpedia.report_volume_up_average(symbol[0], market, to_tail, symbol[1])
        above_avg_counter+= result == 1  

    print(f"{above_avg_counter}/{len(list_symbols)} are above  the average volume.")

def process_rsi_oversold():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.report_rsi_oversold(symbol[0],"tradfi", symbol[1])

def process_rsi_overbought():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.report_rsi_overbought(symbol[0],"tradfi", symbol[1])

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

def process_bb_outside_range(market):
    if market == "tradfi":
        list_symbols = sqlite_lib.get_stock_symbols_list()
    elif market == "crypto":
        list_symbols = sqlite_lib.get_crypto_symbols_list()

    up_counter = 0
    low_counter = 0
    for symbol in list_symbols:
        result = reportpedia.report_bb_bands_outside(symbol[0], market, symbol[1])
        low_counter += result == 1  
        up_counter += result == 2 

    tabulate_lib.print_it_line_white(f"Lower: {low_counter} | Upper: {up_counter}  --> Total: {len(list_symbols)} ")


def process_candles(market):
    print(f"Running candles report for {market} ....")
    reportpedia.report_candles(market)

def process_sp500_reports():
    sp500_reports.print_sp500_reports()