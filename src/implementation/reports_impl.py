from src.implementation.reports import reportpedia
from src.libs import sqlite_lib

def report_ma_50():
    list_symbols = sqlite_lib.get_stock_symbols_list()
    for symbol in list_symbols:
        reportpedia.report_ma_up_down(symbol[0],50)