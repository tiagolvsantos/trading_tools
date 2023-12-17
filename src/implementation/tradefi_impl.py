from src.implementation.tradefi import tradefipedia

def get_market_breath():
    tradefipedia.get_market_breath_table()

def get_market_top_gainers():
    tradefipedia.get_stock_top_gainers()

def get_market_top_loosers():
    tradefipedia.get_stock_top_loosers()

def get_most_active_equity_options():
    tradefipedia.get_equity_active_options()

def get_most_active_index_options():
    tradefipedia.get_index_active_options()

def get_intraday_top_volume():
    tradefipedia.get_intraday_top_volume()

def get_stock_ratings(symbol):
    tradefipedia.get_stock_ratings(symbol)

def get_etf_top_holdings(symbol):
    tradefipedia.get_etf_top_holdings(symbol)

def get_options_ratios():
    tradefipedia.get_options_ratios()

def get_wsb_trending_stocks():
    tradefipedia.get_wsb_trending_stocks()