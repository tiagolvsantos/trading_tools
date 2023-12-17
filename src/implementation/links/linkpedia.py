from src.libs import tabulate_lib
import pandas as pd


def get_all_links():
    data = [['https://roic.ai/quote/AAPL', 'Company financial analysis platform','TradeFi'], 
            ['http://www.openinsider.com/', 'Insiders transactions', 'TradeFi'], 
            ['https://www.capitoltrades.com/trades', 'US Capitol Senators and congressman trades', 'TradeFi'], 
            ['https://finviz.com/map.ashx', 'Market Heatmap', 'TradeFi'], 
            ['https://cib.societegenerale.com/fileadmin/indices_feeds/ti_screen/index.html', 'SocGen CTA Dashboard', 'TradeFi'],
            ['https://seekingalpha.com/author/john-vincent', 'Earnings reviews', 'TradeFi'],  
            ['https://www.marketwatch.com/tools/options-expiration-calendar', 'OPEX Calendar', 'TradeFi'], 
            ['https://www.investing.com/central-banks/', 'Central Banks rates', 'TradeFi'], 
            ['https://cathiesark.com/arkk/trades', 'ARK Funds tracker', 'TradeFi'], 
            ['https://miltonfmr.com/hedge-fund-letters/', 'Hedge funds letters', 'TradeFi'], 
            ['https://charts.bitbo.io/beam/', 'BTC BEAM Chart', 'Crypto'], 
            ['https://charts.bitbo.io/mayer-multiple/', 'BTC Mayer Multiple ', 'Crypto'], 
            ['https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html', 'TOP 100 BTC addresses', 'Crypto']

            ]
    
    df_data = pd.DataFrame(data, columns=['Link', 'Description','Market'])
    tabulate_lib.tabulate_it("Useful links",df_data)