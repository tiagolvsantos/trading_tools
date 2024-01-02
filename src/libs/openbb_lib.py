from openbb_terminal.sdk import openbb
from src.libs import utils
import pandas as pd
import datetime
import os
from datetime import datetime
#openbb.keys.mykeys(show = True)
# help(openbb.keys.twitter)
# openbb.keys.quandl(key = os.environ["QUANDL_AUTH"],persist = True,)
# openbb.keys.fmp(key = os.environ["FINANCIALMODELINGPREP"],persist = True,)
# openbb.keys.finnhub(key = os.environ["FINNHUB_KEY"],persist = True,)
# openbb.keys.fred(key = os.environ["FRED"],persist = True,)
# openbb.keys.av(key = os.environ["ALPHAVANTAGE"], persist = True)

6
## LEGACY

# OVERVIEW
def get_sp500_sector_comparisson_daily():
    spdr_sectors = ['SPY', 'XLE', 'XLB', 'XLI', 'XLP', 'XLY', 'XLV', 'XLF', 'XLK', 'XLC', 'XLU', 'XLRE']
    quotes: object = []
    symbols = spdr_sectors
    for symbols in symbols:
        quote = openbb.stocks.quote(symbols).transpose()
        quotes.append(quote)
    return pd.concat(quotes)

def get_todays_earnings():
    earnings = openbb.stocks.disc.upcoming()
    earnings.index = earnings.index.strftime('%Y-%m-%d')
    return earnings.filter(like =datetime.datetime.now().strftime('%Y-%m-%d'), axis = 0)

def get_dp_borrow_fees():
    return openbb.stocks.dps.ctb()

def get_dps_activity():
    pos_high = openbb.stocks.dps.pos()
    pos_high = pos_high.convert_dtypes()
    pos_high.set_index('Date', inplace = True)
    pos_low = openbb.stocks.dps.pos(ascend = True)
    pos_low = pos_low.convert_dtypes()
    pos_low.set_index('Date', inplace = True)
    pos_df = pd.concat([pos_low,pos_high])
    pos_df.sort_values(by=['Dark Pools Position $'], ascending = False, inplace = True)
    return pos_df

def get_highest_shorted_stocks():
    return openbb.stocks.dps.hsi()

def get_recent_ipos():
    return openbb.stocks.disc.pipo()

def get_daily_gainers():
    return openbb.stocks.disc.gainers()

def get_daily_loosers():
    return openbb.stocks.disc.losers()

def get_retail_sentimentt():
    return openbb.stocks.disc.rtat()

def search_news(search_statement: str):
    return openbb.news(search_statement, "", "published")

def get_sector_performance():
    return openbb.economy.performance(group = 'sector')

def get_econ_calendar():
    return openbb.economy.events()

def get_global_bonds():
    return openbb.economy.glbonds()

def get_us_bonds():
    return openbb.economy.usbonds()

def get_global_overview():
    return openbb.economy.overview()

def get_sp500_sector_performance():
    return openbb.economy.rtps()

def get_sp500_sector_performance_spectrum():
    return openbb.economy.spectrum( "sector", "")

def get_intraday_trading_volume():
    return openbb.stocks.disc.active()

def get_ark_trades():
    return openbb.stocks.disc.arkord( False, False, "")

def get_next_ipos():
    return openbb.stocks.disc.fipo( 25,  None)

def get_list_tech_stocks_earnings_growth_bigger_25_pct():
    return  openbb.stocks.disc.gtech()

def get_hot_penny_stocks():
    return openbb.stocks.disc.hotpenny()

def get_low_floats():
    return openbb.stocks.disc.lowfloat()

def get_top10_retail_stocks():
    return openbb.stocks.disc.rtat()

def get_list_stocks_growth_bigger_25_pct_low_pe_and_peg_ratios():
    return openbb.stocks.disc.ugs()

def get_undervalued_large_cap_stocks():
    return openbb.stocks.disc.ulc()

def get_stocks_congress_last_trades():
    return openbb.stocks.gov.lasttrades("congress", -1, "")

def get_stocks_senate_last_trades():
    return openbb.stocks.gov.lasttrades("senate ", -1, "")

def get_stocks_house_last_trades():
    return openbb.stocks.gov.lasttrades("house", -1, "")

def get_stocks_congress_top_buys():
    return openbb.stocks.gov.topbuys("congress", 6)

def get_stocks_senate_top_buys():
    return openbb.stocks.gov.topbuys("senate", 6)

def get_stocks_house_top_buys():
    return openbb.stocks.gov.topbuys("house", 6)

def get_stocks_congress_top_sells():
    return openbb.stocks.gov.topsells("congress", 6)

def get_stocks_senate_top_sells():
    return openbb.stocks.gov.topsells("senate", 6)

def get_stocks_house_top_sells():
    return openbb.stocks.gov.topsells("house", 6)

def get_sector_valuations():
    return openbb.economy.valuation("sector", "MarketCap", True)

# STOCK INFO

def get_stock_congress_trades(symbol: str):
    return openbb.stocks.gov.gtrades(symbol,  "congress", 6)

def get_stock_senate_trades(symbol: str):
    return openbb.stocks.gov.gtrades(symbol,  "senate", 6)

def get_stock_house_trades(symbol: str):
    return openbb.stocks.gov.gtrades(symbol,  "house", 6)

def get_stock_government_contracts(symbol:str):
    return openbb.stocks.gov.histcont(symbol)

def get_stock_trading_summary(symbol: str):
    return openbb.stocks.ta.summary(symbol)

def get_tv_stock_ta_recomendation(symbol: str):
    return openbb.stocks.ta.recom(symbol,"america", "", "")

def get_bid_ask_spread(symbol:str):
    bid,ask = openbb.stocks.tob(symbol)
    return bid.join(ask, lsuffix= ': Bid', rsuffix = ': Ask')

def get_insider_transactions(symbol:str):
    return openbb.stocks.ins.lins(symbol = symbol)

def get_asset_sentiment_analysis(symbol:str):
    return openbb.stocks.ba.headlines(symbol)

def get_income_comparisson(lst_stocks:list):
    return openbb.stocks.ca.income(similar = lst_stocks, quarter = True)

def get_balance_comparisson(lst_stocks:list):
    return openbb.stocks.ca.balance(lst_stocks)

def get_sentiment_comparisson(lst_stocks:list):
    return openbb.stocks.ca.sentiment(lst_stocks)

def get_price_vs_short_interest(symbol:str):
    spos = openbb.stocks.dps.spos(symbol)
    spos.rename(columns = {'dates':'date'}, inplace= True)
    spos.set_index(keys = 'date', inplace =True)
    psi,price = openbb.stocks.dps.psi_sg(symbol)
    psi.set_index('date', inplace = True)
    spos = psi.join(spos)
    return spos

def get_stock_shareholders(symbol:str):
    return openbb.stocks.fa.shrs(symbol)

def get_stock_enterprise_value(symbol:str):
    return openbb.stocks.fa.enterprise(symbol)

def get_stock_historical_data(symbol: str, from_date:str, to_date:str):
    return openbb.stocks.load(symbol, from_date, 1440, to_date, False, "YahooFinance", "ytd",  False, False, True)    

def get_stock_analyst_ratings(symbol :str):
    return openbb.stocks.dd.analyst(symbol)

def get_stock_dd_forward_estimates(symbol:str):
    return openbb.stocks.dd.est(symbol)

def get_stock_suppliers(symbol:str):
    return openbb.stocks.dd.supplier(symbol, 50)

def get_capm_stock_model(symbol: str):
    return openbb.stocks.qa.capm(symbol)


# FUTURES
def get_futures_symbols():
    return openbb.futures.search("","","")

def get_futures_curve(symbol:str):
    return openbb.futures.curve(symbol)

def get_indices_list():
    return pd.DataFrame.from_dict(openbb.economy.available_indices()).transpose()



# FX
def get_forward_rates(to_currency:str, from_currency:str):
    return openbb.forex.fwd(to_currency , from_currency)

def get_fx_historicaldata(to_currency:str, from_currency:str):
    return openbb.forex.load(to_currency, from_currency, "d",  "1day",  None,  "YahooFinance", False)

def get_fx_symbols_list():
    return openbb.forex.get_currency_list()



# OPTIONS
def get_options_expirations(symbol:str):
    return openbb.stocks.options.expirations(symbol, "Nasdaq")

def get_options_greeks(symbol:str, expiration_date: str, strike:str):
    return openbb.stocks.options.grhist(symbol, expiration_date, strike, "",  False)  

def get_asset_pcr(symbol: str, start_date: str):
    pcr = openbb.stocks.options.pcr(symbol = symbol, start_date = start_date)
    pcr.rename(columns = {'PCR': 'Put/Call Ratio'})
    return pcr

def get_options_vsurf(symbol: str):
    return openbb.stocks.options.vsurf(symbol)

def get_unusual_options_activity(number_of_records: int):
    return openbb.stocks.options.unu(number_of_records)   

def get_options_historical_data(symbol: str, expiration_date:str, strike: str):
    return openbb.stocks.options.hist_ce( symbol, expiration_date,  True,  strike)



# ETF
def get_etf_overview(symbol: str):
    return openbb.etf.overview(symbol)

def get_etf_holdings(symbol: str):
    return openbb.etf.holdings(symbol)





# PLOTS
def plot_indices_list(indices_list: list):
    return openbb.economy.index_chart(indices = indices_list, start_date=f"{datetime.now().year }-01-01")

# Interval -> (in minutes) to get data 1, 5, 15, 30, 60 or 1440
# prepost -> Pre and After hours data
# https://docs.openbb.co/sdk/reference/stocks/candle
def plot_ma_asset_chart(symbol :str, interval: int, prepost:bool):
    return openbb.stocks.candle(symbol, ma = [50,100,200], add_trend= True, interval = interval, prepost=prepost, start_date= f"{datetime.now().year -1}-01-01")

def plot_asset_chart(symbol :str, interval=1440, prepost=True):
    return openbb.stocks.candle(symbol, add_trend= True, interval = interval, prepost=prepost, start_date= f"{datetime.now().year -1}-01-01")


def plot_ma_fx_chart(df_data ,to_currency:str, from_currency:str ):
    return openbb.forex.candle(df_data, to_currency , from_currency,  [50,100,200],  None,  True,  False, "linear")

def plot_crypto(asset:str):
    openbb.crypto.candle(symbol=asset, start_date=f"{datetime.now().year -1}-01-01")


## CRYPTO
def get_crypto_market_cap_sectors():
    return openbb.crypto.ov.categories("market_cap_desc")

def get_crypto_exchanges_withdrawal_fees():
    return openbb.crypto.ov.ewf()

def get_crypto_stables_market_cap():
    return openbb.crypto.ov.stables( 15,  "Market_Cap_[$]",False)

def get_crypto_supply_rates():
    return openbb.crypto.ov.cr("supply")

def get_crypto_borrow_rates():
    return openbb.crypto.ov.cr("borrow")



