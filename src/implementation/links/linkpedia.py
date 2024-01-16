from src.libs import tabulate_lib
import pandas as pd


def get_all_links():
    data = [['https://roic.ai/quote/AAPL', 'Company financial analysis platform','TradFi'], 
            ['http://www.openinsider.com/', 'Insiders transactions', 'TradFi'], 
            ['https://www.capitoltrades.com/trades', 'US Capitol Senators and congressman trades', 'TradFi'], 
            ['https://finviz.com/map.ashx', 'Market Heatmap', 'TradFi'], 
            ['https://cib.societegenerale.com/fileadmin/indices_feeds/ti_screen/index.html', 'SocGen CTA Dashboard', 'TradFi'],
            ['https://seekingalpha.com/author/john-vincent', 'Earnings reviews', 'TradFi'],
            ['https://spotgamma.com/free-tools/implied-earnings-moves', 'Implied earnings move', 'TradFi'],    
            ['https://www.marketwatch.com/tools/options-expiration-calendar', 'OPEX Calendar', 'TradFi'], 
            ['https://www.investing.com/central-banks/', 'Central Banks rates', 'TradFi'], 
            ['https://cathiesark.com/arkk/trades', 'ARK Funds tracker', 'TradFi'], 
            ['https://miltonfmr.com/hedge-fund-letters/', 'Hedge funds letters', 'TradFi'], 
            ['https://docs.google.com/spreadsheets/d/1p1aDFolOQnzUOb9rlfdq9QqzkJfB2k0CgES1hOmb2ss/edit?usp=sharing', 'GSheets market dashboard', 'TradFi'], 
            ['https://docs.google.com/spreadsheets/d/1dr-GHEs9d-Q4dzCiM4zeWC0E6Dd1rYX3L9cjIzHC-3U/edit?usp=sharing', 'GSheets 50DMA dashboard', 'TradFi'], 
            ['https://charts.bitbo.io/beam/', 'BTC BEAM Chart', 'Crypto'], 
            ['https://charts.bitbo.io/mayer-multiple/', 'BTC Mayer Multiple ', 'Crypto'], 
            ['https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html', 'TOP 100 BTC addresses', 'Crypto']

            ]
    
    df_data = pd.DataFrame(data, columns=['Link', 'Description','Market'])
    tabulate_lib.tabulate_it("Useful links",df_data)