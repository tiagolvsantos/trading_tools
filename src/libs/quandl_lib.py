import quandl 
from configs import QUANDL_AUTH


def get_sp500_shiller_pe_by_month():
    try:
        return quandl.get(
            "MULTPL/SHILLER_PE_RATIO_MONTH",
            authtoken = QUANDL_AUTH,
        )

    except NameError:
        return NameError

def get_sp500_pe_by_month():
    try:
        return quandl.get(
            "MULTPL/SP500_PE_RATIO_MONTH",
            authtoken = QUANDL_AUTH,
        )

    except NameError:
        return NameError

def get_sp500_dividend_by_month():
    try:
        return quandl.get(
            "MULTPL/SP500_DIV_YIELD_MONTH",
            authtoken = QUANDL_AUTH,
        )

    except NameError:
        return NameError

def get_sp500_inflation_adj_monthly():
    try:
        return quandl.get(
            "MULTPL/SP500_INFLADJ_MONTH",
            authtoken = QUANDL_AUTH,
        )

    except NameError:
        return NameError

def get_sp500_dividend_month():
    try:
        return quandl.get(
            "MULTPL/SP500_DIV_MONTH", authtoken = QUANDL_AUTH
        )

    except NameError:
        return NameError

def get_sp500_sales_growth_by_quarter():
    try:
        return quandl.get(
            "MULTPL/SP500_REAL_SALES_GROWTH_QUARTER",
            authtoken=QUANDL_AUTH,
        )

    except NameError:
        return NameError
    
def get_quandl_data(symbol):
    try:
        return quandl.get(symbol, authtoken=QUANDL_AUTH)
    except NameError:
        return NameError
