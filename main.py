# Import the necessary packages
import inquirer
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
                    choices=['TradeFi', 'Crypto', 'Charts', 'Reports', 'Interactive','Links','Jobs','Exit'],
                    carousel=True
                ),
    ]
    return inquirer.prompt(main_menu)

def tradefi_menu():
    tradefi_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['Market Breath', 'Top gainers', 'Top loosers', 'Most active equity Options', 'Most active index options',
                             'Intraday top volume','Stock ratings','ETF top holdings','Options ratios','Fear Greed Index',
                             'WSB Trending stocks for the last 12h', "Stock News", "Stock insider trading","SP500 stocks technicals",
                             'Main menu'],
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
    if tradefi_menu_pick["option"] == "Stock News":
        tradefi_impl.get_stock_news(input("Select a symbol:"))
    if tradefi_menu_pick["option"] == "Stock insider trading":
        tradefi_impl.get_stock_insider_trading(input("Select a symbol:"))
    if tradefi_menu_pick["option"] == "SP500 stocks technicals":
        tradefi_impl.get_sp500_technicals()
    if tradefi_menu_pick["option"] == "ETF top holdings":
        tradefi_impl.get_etf_top_holdings(input("Select a symbol:"))
    if tradefi_menu_pick["option"] == "Options ratios":
        tradefi_impl.get_options_ratios()   
    if tradefi_menu_pick["option"] == "Fear Greed Index":
        charts_impl.chart_fear_greed()
    if tradefi_menu_pick["option"] == "WSB Trending stocks for the last 12h":
        tradefi_impl.get_wsb_trending_stocks()
    if tradefi_menu_pick["option"] == "Main menu":
        main()
    main()

def interactive_menu():
    interactive_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['Binance abnormal Trading', 'Binance Agg Trades', 'BitMEX Agg Trades','Main menu'],
                    carousel=True
                ),
    ]
    interactive_menu_pick = inquirer.prompt(interactive_menu)
    if interactive_menu_pick["option"] == "Binance abnormal Trading":
       interactive_impl.bina_abnormal_trading_impl()
    if interactive_menu_pick["option"] == "Binance Agg Trades":
        interactive_impl.bina_ws_agg_trades_impl(input("Select a symbol:"),input("Select a threshold:"))
    if interactive_menu_pick["option"] == "BitMEX Agg Trades":
        interactive_impl.bitmex_ws_agg_trades_impl(input("Select a symbol:"))
    if interactive_menu_pick["option"] == "Main menu":
        main()
    main()

def charts_menu():
    charts_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=["TA", "MAG7","Asset profile","Cross asset corr",
                             "SPX/VIX ratio","SPX 2D RSI", "VIX 1 ATR","Futures curve", 
                             "ETF Flows","Crypto CVD","S/R TradeFi","S/R Crypto", 'ShortVol chart',
                             'Options charts', 'Srategic Petroleum Reserve','Google trends', 'Year on Year comparrison'
                             'Main menu'],
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
    if charts_menu_pick["option"] == "S/R TradeFi":
        charts_impl.chart_sr_tradefi(input("Select a symbol:").upper())
    if charts_menu_pick["option"] == "S/R Crypto":
        charts_impl.chart_sr_crypto(input("Select a symbol:").upper())
    if charts_menu_pick["option"] == "ETF Flows":
        charts_impl.chart_etf_flows(input("Select a symbol:").upper())
    if charts_menu_pick["option"] == "ShortVol chart":
        charts_impl.chart_simple_chart('^SHORTVOL')
    if charts_menu_pick["option"] == "Srategic Petroleum Reserve":
        charts_impl.chart_spr()
    if charts_menu_pick["option"] == "Google trends":
        input_string = input('Enter elements to search separated by space \n')
        lst_keywords = input_string.split()
        charts_impl.chart_google_trends(lst_keywords)
    if charts_menu_pick["option"] == "Options charts":
        charts_impl.chart_options_data(input("Select a symbol:").upper())
    if charts_menu_pick["option"] == "Year on Year comparrison":
        charts_impl.chart_year_on_year_comparisson(input("Select a symbol:").upper(),input("Select a year:").upper())
    if charts_menu_pick["option"] == "Main menu":
        main()
    main()
    
def crypto_menu():
    crypto_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['Binance Order Flow',"Trending tokens","Companies holding crypto","Fear Greed index",'Main menu'],
                    carousel=True
                ),
    ]
    crypto_menu_pick = inquirer.prompt(crypto_menu)
    if crypto_menu_pick["option"] == "Binance Order Flow":
        crypto_impl.plot_binance_flows_for_asset(input("Select a symbol:").upper())
    if crypto_menu_pick["option"] == "Trending tokens":
        crypto_impl.get_trending_tokens()
    if crypto_menu_pick["option"] == "Companies holding crypto":
        crypto_impl.get_companies_holding_crypto()
    if crypto_menu_pick["option"] == "Fear Greed index":
        charts_impl.chart_crypto_fear_greed()
    if crypto_menu_pick["option"] == "Main menu":
        main()
    main()

def links_menu():
    links_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['Research links','Main menu'],
                    carousel=True
                ),
    ]
    links_menu_pick = inquirer.prompt(links_menu)
    if links_menu_pick["option"] == "Research links":
        links_impl.get_links_list()
    if links_menu_pick["option"] == "Main menu":
        main()
    main()

def reports_menu():
    reports_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['50 MA up/down TradeFi','50 MA up/down Crypto','200 EMA up/down TradeFi',
                             '200 EMA up/down Crypto','Volume bigger than average TradeFi',
                             'Volume bigger than average Crypto','RSI Overbought',
                             'RSI Oversold','CoT Reports','Main menu'],
                    carousel=True
                ),
    ]
    reports_menu_pick = inquirer.prompt(reports_menu)
    if reports_menu_pick["option"] == "50 MA up/down TradeFi":
        reports_impl.report_ma(50, "tradefi")
    if reports_menu_pick["option"] == "50 MA up/down Crypto":
        reports_impl.report_ma(50, "crypto")
    if reports_menu_pick["option"] == "200 EMA up/down Crypto":
        reports_impl.report_ema(200, "crypto")
    if reports_menu_pick["option"] == "200 EMA up/down TradeFi":
        reports_impl.report_ema(200, "tradefi")
    if reports_menu_pick["option"] == "Volume bigger than average TradeFi":
        reports_impl.process_volume_average("tradefi")
    if reports_menu_pick["option"] == "Volume bigger than average Crypto":
        reports_impl.process_volume_average("crypto")
    if reports_menu_pick["option"] == "RSI Overbought":
        reports_impl.process_rsi_overbought()
    if reports_menu_pick["option"] == "RSI Oversold":
        reports_impl.process_rsi_oversold()
    if reports_menu_pick["option"] == "CoT Reports":
        reports_impl.process_cot_reports()
    if reports_menu_pick["option"] == "Main menu":
        main()

    main()

def jobs_menu():
    jobs_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['Process strategies','main'],
                    carousel=True
                ),
    ]
    jobs_menu_pick = inquirer.prompt(jobs_menu)
    if jobs_menu_pick["option"] == "Process strategies":
        reports_impl.run_jobs()
    if jobs_menu_pick["option"] == "Main menu":
        main()
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
    if main_menu_pick["option"] == "Exit":
        exit()
    print("\n")

if __name__ == "__main__":
    #configure_env_vars()
    main()
    print("\n")
  
