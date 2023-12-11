# Import the necessary packages
import inquirer
from src.implementation.interactive import bina_ws_agg_trades 
from src.implementation.interactive import bina_abnormal_trading 
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
       bina_abnormal_trading.main()
    if interactive_menu_pick["option"] == "Binance Agg Trades":
        bina_ws_agg_trades.main(input("Select a symbol:"),input("Select a threshold:"))
    

def main():
    main_menu_pick = main_menu()
    if main_menu_pick["option"] == "TradeFi":
        print("TradeFi")
    if main_menu_pick["option"] == "Crypto":
        print("Crypto")
    if main_menu_pick["option"] == "Charts":
        print("Charts")
    if main_menu_pick["option"] == "Reports":
        print("Reports")
    if main_menu_pick["option"] == "Interactive":
        interactive_menu()


if __name__ == "__main__":
    main()
