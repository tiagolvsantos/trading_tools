# Import the necessary packages
import inquirer
from env_vars import configure_env_vars
from src.implementation import interactive_impl 
from src.implementation import charts_impl
## Menus
def main_menu():
    main_menu = [
    inquirer.List('option',
                    message="Select an option",
                    choices=['TradeFi', 'Crypto', 'Charts', 'Reports', 'Interactive'],
                    carousel=True
                ),
    ]
    return inquirer.prompt(main_menu)


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
                             "SPX/VIX ratio","SPX 2D RSI", "VIX 1 ATR","Futures curve"],
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
    main()
        # bina_ws_agg_trades.main(input("Select a symbol:"),input("Select a threshold:"))


def main():
    main_menu_pick = main_menu()
    if main_menu_pick["option"] == "TradeFi":
        print("TradeFi")
    if main_menu_pick["option"] == "Crypto":
        print("Crypto")
    if main_menu_pick["option"] == "Charts":
        charts_menu()
    if main_menu_pick["option"] == "Reports":
        print("Reports")
    if main_menu_pick["option"] == "Interactive":
        interactive_menu()


if __name__ == "__main__":
    #configure_env_vars()
    main()
