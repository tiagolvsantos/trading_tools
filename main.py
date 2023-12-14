# Import the necessary packages
import inquirer
from env_vars import configure_env_vars
from src.implementation import interactive_impl 
from src.implementation import charts_impl
from src.implementation import tradefi_impl
from src.implementation import crypto_impl
from src.implementation import links_impl
from src.implementation import reports_impl
## Menus
def main_menu():
    main_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['TradeFi', 'Crypto', 'Charts', 'Reports', 'Interactive','Links','Jobs'],
                    carousel=True
                ),
    ]
    return inquirer.prompt(main_menu)

def tradefi_menu():
    tradefi_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['Market Breath', 'Top gainers', 'Top loosers', 'Most active equity Options', 'Most active index options',
                             'Intraday top volume','Stock ratings'],
                    carousel=True
                ),
    ]
    tradefi_menu_pick = inquirer.prompt(tradefi_menu)
    if tradefi_menu_pick["option"] == "Market Breath":
        tradefi_impl.get_market_breath()
    if tradefi_menu_pick["option"] == "Top gainers":
        tradefi_impl.get_market_top_gainers()
    if tradefi_menu_pick["option"] == "Top loosers":
        tradefi_impl.get_market_top_loosers()
    if tradefi_menu_pick["option"] == "Most active equity Options":
        tradefi_impl.get_most_active_equity_options()
    if tradefi_menu_pick["option"] == "Most active index options":
        tradefi_impl.get_most_active_index_options()
    if tradefi_menu_pick["option"] == "Intraday top volume":
        tradefi_impl.get_intraday_top_volume()
    if tradefi_menu_pick["option"] == "Stock ratings":
        tradefi_impl.get_stock_ratings(input("Select a symbol:"))
    
    main()

def interactive_menu():
    interactive_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['Binance abnormal Trading', 'Binance Agg Trades'],
                    carousel=True
                ),
    ]
    interactive_menu_pick = inquirer.prompt(interactive_menu)
    if interactive_menu_pick["option"] == "Binance abnormal Trading":
       interactive_impl.bina_abnormal_trading_impl()
    if interactive_menu_pick["option"] == "Binance Agg Trades":
        interactive_impl.bina_ws_agg_trades_impl(input("Select a symbol:"),input("Select a threshold:"))
    main()

def charts_menu():
    charts_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=["TA", "MAG7","Asset profile","Cross asset corr",
                             "SPX/VIX ratio","SPX 2D RSI", "VIX 1 ATR","Futures curve","Crypto CVD"],
                    carousel=True
                ),
    ]
    charts_menu_pick = inquirer.prompt(charts_menu)
    if charts_menu_pick["option"] == "TA":
        charts_impl.chart_general_ta_impl(input("Select a symbol:").upper())
    if charts_menu_pick["option"] == "MAG7":
        charts_impl.chart_general_ta_mag7_impl()
    if charts_menu_pick["option"] == "Asset profile":
        charts_impl.chart_asset_profile_impl(input("Select a symbol:").upper())
    if charts_menu_pick["option"] == "Cross asset corr":
        charts_impl.chart_cross_asset_correlation_impl()
    if charts_menu_pick["option"] == "SPX/VIX ratio":
        charts_impl.chart_sp500_vix_impl()
    if charts_menu_pick["option"] == "SPX 2D RSI":
        charts_impl.chart_spx_2d_rsi_impl()
    if charts_menu_pick["option"] == "VIX 1 ATR":
        charts_impl.chart_vix_atr_1_impl()
    if charts_menu_pick["option"] == "Futures curve":
        charts_impl.chart_futures_curve_impl(input("Select a symbol:").upper())
    if charts_menu_pick["option"] == "Crypto CVD":
        charts_impl.chart_binance_symbol_cvd(input("Select a symbol:").upper(),"1d",180)
    main()

def crypto_menu():
    crypto_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['Binance Order Flow'],
                    carousel=True
                ),
    ]
    crypto_menu_pick = inquirer.prompt(crypto_menu)
    if crypto_menu_pick["option"] == "Binance Order Flow":
        crypto_impl.plot_binance_flows_for_asset(input("Select a symbol:").upper())


    main()

def links_menu():
    links_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['Research links'],
                    carousel=True
                ),
    ]
    links_menu_pick = inquirer.prompt(links_menu)
    if links_menu_pick["option"] == "Research links":
        links_impl.get_links_list()

    main()

def reports_menu():
    reports_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['50 MA up/down','Volume bigger than average'],
                    carousel=True
                ),
    ]
    reports_menu_pick = inquirer.prompt(reports_menu)
    if reports_menu_pick["option"] == "50 MA up/down":
        reports_impl.report_ma(50)
    if reports_menu_pick["option"] == "Volume bigger than average":
        reports_impl.process_volume_average()
    main()

def jobs_menu():
    reports_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['Reports MA'],
                    carousel=True
                ),
    ]
    reports_menu_pick = inquirer.prompt(reports_menu)
    if reports_menu_pick["option"] == "Reports MA":
        reports_impl.run_jobs()

    main()
def main():
    main_menu_pick = main_menu()
    if main_menu_pick["option"] == "TradeFi":
        tradefi_menu()
    if main_menu_pick["option"] == "Crypto":
        crypto_menu()
    if main_menu_pick["option"] == "Charts":
        charts_menu()
    if main_menu_pick["option"] == "Reports":
        reports_menu()
    if main_menu_pick["option"] == "Interactive":
        interactive_menu()
    if main_menu_pick["option"] == "Links":
        links_menu()
    if main_menu_pick["option"] == "Jobs":
        jobs_menu()

if __name__ == "__main__":
    #configure_env_vars()
    main()
  
