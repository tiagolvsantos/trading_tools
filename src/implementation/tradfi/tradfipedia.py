from src.libs import wsj_lib
from src.libs import tabulate_lib
from src.libs import openbb_lib
from src.libs import CBOE_lib
from src.libs import webull_lib
from src.libs import trackinsight_lib
from src.libs import swaggystocks_lib
from src.libs import finviz_lib
from src.libs import utils
import pandas as pd


def get_market_breath_table():
    """
    Retrieves market breath data from the wsj_lib module and displays it using tabulate_lib.

    Returns:
        None
    """
    df_data = wsj_lib.get_market_breath()
    if len(df_data) > 0:
        tabulate_lib.tabulate_it("MARKET BREATH", df_data)
    df_data = wsj_lib.get_market_high_low()
    if len(df_data) > 0:
        tabulate_lib.tabulate_it("MARKET HIGH / LOW", df_data)
    df_data = wsj_lib.get_market_volume()
    if len(df_data) > 0:
        tabulate_lib.tabulate_it("MARKET VOLUME", df_data)


def get_stock_top_gainers():
    """
    Retrieves the daily top gainers in the stock market.

    Returns:
        None
    """
    df_data = openbb_lib.get_daily_gainers()
    if len(df_data) > 0:
        tabulate_lib.tabulate_it("Daily gainers", df_data.reset_index())


def get_stock_top_loosers():
    """
    Retrieves the daily top losers in the stock market.

    Returns:
        None
    """
    df_data = openbb_lib.get_daily_loosers()
    if len(df_data) > 0:
        tabulate_lib.tabulate_it("Daily loosers", df_data.reset_index())

def get_equity_active_options():
    """
    Retrieves and processes active equity options data.

    Returns:
        None
    """
    data = CBOE_lib.get_equity_active_options()
    if len(data) > 0:   
        df_calls = CBOE_lib.parse_cbe_list(data["calls"]) 
        df_calls = df_calls[df_calls.columns[::-1]]
        df_calls['side'] = 'Call'
        df_puts = CBOE_lib.parse_cbe_list(data["puts"]) 
        df_puts.insert (0, 'side', 'Put')
        df_merged = pd.concat([df_calls, df_puts], axis=1)
        tabulate_lib.tabulate_it("MOST ACTIVE EQUITY OPTIONS", df_merged)
    else:
        print("No data!")

def get_index_active_options():
    """
    Retrieves the most active index options data from CBOE and displays it.

    This function fetches the most active index options data from the CBOE library,
    parses the data for calls and puts, and then merges them into a single DataFrame.
    The merged DataFrame is then displayed using the `tabulate_it` function.

    If no data is available, it prints "No data!".

    Returns:
        None
    """
    data = CBOE_lib.get_index_active_options()
    if len(data) > 0: 
        df_calls = CBOE_lib.parse_cbe_list(data["calls"]) 
        df_calls = df_calls[df_calls.columns[::-1]]
        df_calls['side'] = 'Call'
        df_puts = CBOE_lib.parse_cbe_list(data["puts"]) 
        df_puts.insert (0, 'side', 'Put')
        df_merged = pd.concat([df_calls, df_puts], axis=1)
        tabulate_lib.tabulate_it("MOST ACTIVE INDEX OPTIONS", df_merged)
    else:
        print("No data!")

def get_intraday_top_volume():
    """
    Retrieves intraday trading volume data and displays it using tabulate_lib.

    Returns:
        None
    """
    df_data = openbb_lib.get_intraday_trading_volume()
    if len(df_data) > 0: 
        tabulate_lib.tabulate_it("Intraday Top Volume", df_data)

def get_stock_ratings(symbol):
    """
    Retrieves and prints the market ratings and price targets for a given stock symbol.

    Args:
        symbol (str): The stock symbol to retrieve ratings for.

    Returns:
        None
    """
    data = webull_lib.get_analysis(symbol.upper())
    if len(data) > 1 and not ('code' in data and data['code'] == 'INTERNAL_SERVER_ERROR'):
        # Your code here
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
    """
    Retrieves the top holdings of an ETF based on its symbol.

    Args:
        symbol (str): The symbol of the ETF.

    Returns:
        dict: A dictionary containing the top holdings of the ETF.

    """
    tabulate_lib.tabulate_dict(trackinsight_lib.get_etf_x_ray(symbol)) if trackinsight_lib.get_etf_x_ray(symbol) else None

def get_options_statistics():
    """
    Retrieves options statistics data and prints it.

    This function retrieves options statistics data using the `get_options_ratios` function from the `CBOE_lib` module.
    If the retrieved data is not empty, it prints the data using the `print_it_line_title` function from the `tabulate_lib` module.
    For each row in the data, it calls the `_get_options_statistics_compute_data` function passing the data and the row index.
    If the retrieved data is empty, it prints "No data on weekends!".
    """
    df_data = CBOE_lib.get_options_ratios()
    if len(df_data) != 0:
        tabulate_lib.print_it_line_title(" \n OPTIONS RATIOS \n ")
        for index, row in df_data.iterrows():
            _get_options_statistics_compute_data(df_data, index)
    else:
        print("No data on weekends!")
    print("\n")

def _get_options_statistics_compute_data(df_data, index):
    df_data.at[index,'Equity Option Contracts']= utils.print_formated_numbers(float(df_data.at[index,'Equity Option Contracts']))
    df_data.at[index,'Equity Option Notional']= utils.print_formated_numbers(float(df_data.at[index,'Equity Option Notional']))
    df_data.at[index,'Index/Other Option Contracts']= utils.print_formated_numbers(float(df_data.at[index,'Index/Other Option Contracts']))
    df_data.at[index,'Index/Other Option Notional']= utils.print_formated_numbers(float(df_data.at[index,'Index/Other Option Notional']))
    df_data.at[index,'Total Option Contracts']= utils.print_formated_numbers(float(df_data.at[index,'Total Option Contracts']))
    df_data.at[index,'Total Option Notional']= utils.print_formated_numbers(float(df_data.at[index,'Total Option Notional']))
    tabulate_lib.tabulate_it("CBOE Options Ratios",df_data)

def get_wsb_trending_stocks():
    tabulate_lib.tabulate_it("WSB Trending stocks for the last 12h", swaggystocks_lib.get_wsb_buzz_stocks()) if swaggystocks_lib.get_wsb_buzz_stocks() else None

def get_stock_news(symbol):
    tabulate_lib.tabulate_it(f'News for {symbol}', finviz_lib.symbol_news(symbol)) if finviz_lib.symbol_news(symbol) else None

def get_stock_insider_trading(symbol):
    tabulate_lib.tabulate_it(f'Insider trading for {symbol}', finviz_lib.symbol_insider_trading(symbol)) if finviz_lib.symbol_insider_trading(symbol) else None

def get_sp500_technicals():
    tabulate_lib.tabulate_it('SP500 technicals', finviz_lib.get_technicals()) if finviz_lib.get_technicals() else None

def get_options_ratios():
    """
    Retrieves options ratios from CBOE library and prints them using tabulate_lib.

    Returns:
        None
    """
    json_data = CBOE_lib.get_options_ratios()
    if len(json_data) != 0:
        tabulate_lib.print_it_line_title(" \n OPTIONS RATIOS \n ")
        yesterday_date = utils.get_yesterdays_date("%Y-%m-%d")
        for ratio in json_data["ratios"]:
            tabulate_lib.print_it_line(f"Date: {yesterday_date}")
            tabulate_lib.print_it_line(f"{ratio['name']}: {ratio['value']} ")
    else:
        print("No data on weekends!")
    print("\n")