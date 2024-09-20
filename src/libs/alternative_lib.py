import requests
import yfinance as yf
import pandas as pd


def get_crypto_fear_greed_index():
    url = "https://api.alternative.me/fng/?limit=10"
    try:
        return requests.get(url).json()
    except Exception:
        return {}
    

def get_sp500_top5_stocks_per_sector():
    # Fetch the list of S&P 500 stocks
    sp500_symbols = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()

    # Retrieve sector information and market cap for each stock
    stocks_data = []
    for symbol in sp500_symbols:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        stocks_data.append({
            'symbol': symbol,
            'sector': info.get('sector', 'Unknown'),
            'market_cap': info.get('marketCap', 0)
        })

    # Convert to DataFrame
    df = pd.DataFrame(stocks_data)

    # Filter out stocks with missing sector or market cap
    df = df[df['sector'] != 'Unknown']
    df = df[df['market_cap'] > 0]

    # Sort stocks within each sector by market capitalization
    df = df.sort_values(by=['sector', 'market_cap'], ascending=[True, False])

    # Select the top 5 stocks for each sector
    top_stocks_per_sector = df.groupby('sector').head(5)

    # Print the result
    #print(top_stocks_per_sector)
    return top_stocks_per_sector