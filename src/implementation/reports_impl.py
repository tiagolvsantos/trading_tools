from src.implementation.reports import reportpedia
from src.libs import sqlite_lib

def process_ma_50():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.process_ma_up_down(symbol[0],50)

def process_ma_100():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.process_ma_up_down(symbol[0],100)

def process_ma_200():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.process_ma_up_down(symbol[0],200)

def report_ma(ma):
    reportpedia.report_ma(ma)

def process_volume_average():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.report_volume_up_average(symbol[0])

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
    process_ma_50()
    process_ma_100()
    process_ma_200()
    print("Running jobs done!")

