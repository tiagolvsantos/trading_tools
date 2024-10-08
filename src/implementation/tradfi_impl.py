from src.implementation.tradfi import tradfipedia

def get_market_breath():
    tradfipedia.get_market_breath_table()

def get_most_active_equity_options():
    tradfipedia.get_equity_active_options()

def get_most_active_index_options():
    tradfipedia.get_index_active_options()

def get_etf_top_holdings(symbol):
    tradfipedia.get_etf_top_holdings(symbol)

def get_options_statistics():
    tradfipedia.get_options_statistics()

def get_wsb_trending_stocks():
    tradfipedia.get_wsb_trending_stocks()

def get_stock_news(symbol):
    tradfipedia.get_stock_news(symbol)

def get_stock_insider_trading(symbol):
    tradfipedia.get_stock_insider_trading(symbol)

def get_sp500_technicals():
    tradfipedia.get_sp500_technicals()

def get_options_ratios():
    tradfipedia.get_options_ratios()