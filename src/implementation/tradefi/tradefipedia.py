from src.libs import wsj_lib
from src.libs import tabulate_lib
from src.libs import openbb_lib
from src.libs import CBOE_lib
from src.libs import webull_lib
from src.libs import trackinsight_lib
import pandas as pd


def get_market_breath_table():
    df_data = wsj_lib.get_market_breath()
    tabulate_lib.tabulate_it("MARKET BREATH", df_data)
    df_data = wsj_lib.get_market_high_low()
    tabulate_lib.tabulate_it("MARKET HIGH / LOW", df_data)
    df_data = wsj_lib.get_market_volume()
    tabulate_lib.tabulate_it("MARKET VOLUME", df_data)


def get_stock_top_gainers():
    df_data = openbb_lib.get_daily_gainers()
    tabulate_lib.tabulate_it("Daily gainers", df_data.reset_index())


def get_stock_top_loosers():
    df_data = openbb_lib.get_daily_loosers()
    tabulate_lib.tabulate_it("Daily loosers", df_data.reset_index())

def get_equity_active_options():
    data = CBOE_lib.get_equity_active_options()
    df_calls = CBOE_lib.parse_cbe_list(data["calls"]) 
    df_calls = df_calls[df_calls.columns[::-1]]
    df_calls['side'] = 'Call'
    df_puts = CBOE_lib.parse_cbe_list(data["puts"]) 
    df_puts.insert (0, 'side', 'Put')
    df_merged = pd.concat([df_calls, df_puts], axis=1)
    tabulate_lib.tabulate_it("MOST ACTIVE EQUITY OPTIONS", df_merged)

def get_index_active_options():
    data = CBOE_lib.get_index_active_options()
    df_calls = CBOE_lib.parse_cbe_list(data["calls"]) 
    df_calls = df_calls[df_calls.columns[::-1]]
    df_calls['side'] = 'Call'
    df_puts = CBOE_lib.parse_cbe_list(data["puts"]) 
    df_puts.insert (0, 'side', 'Put')
    df_merged = pd.concat([df_calls, df_puts], axis=1)
    tabulate_lib.tabulate_it("MOST ACTIVE INDEX OPTIONS", df_merged)

def get_intraday_top_volume():
    df_data = openbb_lib.get_intraday_trading_volume()
    tabulate_lib.tabulate_it("Intraday Top Volume", df_data)

def get_stock_ratings(symbol):
  data =webull_lib.get_analysis(symbol)
  if len(data) > 1:
    print(f"MARKET RATING FOR {symbol}")
    print("----------------------------------------------------------------------------")
    print(f"""Market rating: {data['rating']["ratingAnalysis"]}""")
    print(
        f"""     Under Perform: {data['rating']["ratingSpread"]["underPerform"]}"""
    )
    print(f"""     Buy: {data['rating']["ratingSpread"]["buy"]}""")
    print(f"""     Sell: {data['rating']["ratingSpread"]["sell"]}""")
    print(f"""     Strong Buy: {data['rating']["ratingSpread"]["strongBuy"]}""")
    print(f"""     Hold: {data['rating']["ratingSpread"]["hold"]}""")
    print("")
    print("----------------------------------------------------------------------------")
    print("PRICE TARGETS:")
    print(
        f"""Low: {data['targetPrice']["low"]}   High: {data['targetPrice']["high"]}   Mean: {data['targetPrice']["mean"]}   Current: {data['targetPrice']["current"]}"""
    )

def get_etf_top_holdings(symbol):
    tabulate_lib.tabulate_dict(trackinsight_lib.get_etf_x_ray(symbol))