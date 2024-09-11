import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timezone

# Define sector_etfs globally
sector_etfs = {
    'Technology': 'XLK',
    'Healthcare': 'XLV',
    'Financials': 'XLF',
    'Energy': 'XLE',
    'Consumer Discretionary': 'XLY',
    'Consumer Staples': 'XLP',
    'Industrials': 'XLI',
    'Materials': 'XLB',
    'Utilities': 'XLU',
    'Real Estate': 'XLRE',
    'Communication Services': 'XLC'
}

period = 'YTD'

def __get_performance(ticker, period=period):
    """
    Fetch the performance data for a given ticker over a specified period.

    Parameters:
    ticker (str): The ticker symbol.
    period (str): The period over which to fetch the performance data (default is '1y').

    Returns:
    float: The performance percentage.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    performance = (hist['Close'][-1] - hist['Close'][0]) / hist['Close'][0] * 100
    return performance

def __get_52_week_high_low(ticker):
    """
    Fetch the 52-week high and low for a given ticker.

    Parameters:
    ticker (str): The ticker symbol.

    Returns:
    tuple: The 52-week high, 52-week low, and current price.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period='1y')
    high_52_week = hist['High'].max()
    low_52_week = hist['Low'].min()
    current_price = hist['Close'][-1]
    return high_52_week, low_52_week, current_price

def calculate_sp500_sector_std():
    # Dictionary to store standard deviations
    sector_std = {}

    # Fetch historical data and calculate standard deviation of returns
    for sector, etf in sector_etfs.items():
        data = yf.Ticker(etf).history(period=period)  # Adjust period as needed
        returns = data['Close'].pct_change().dropna()
        sector_std[sector] = returns.std()

    # Convert to DataFrame for pretty printing
    sector_std_df = pd.DataFrame.from_dict(sector_std, orient='index', columns=['Standard Deviation'])
    sector_std_df.index.name = 'Sector'
    sector_std_df = sector_std_df.sort_values(by='Standard Deviation', ascending=False)

    print("Higher standard deviation means higher volatility and risk, while lower standard deviation means lower volatility and risk.")
    print("This information helps investors understand the risk associated with different sectors and make informed investment decisions.")
    print(sector_std_df.to_string())
    print("")
    print("")


def check_sector_outperformance():
    """
    Check which sectors are outperforming the S&P 500 using sector ETFs.

    Returns:
    list: A sorted list of sectors that are outperforming the S&P 500, from higher to lower performance.
    """
    sp500_ticker = '^GSPC'

    sp500_performance = __get_performance(sp500_ticker)
    sector_performance = {sector: __get_performance(ticker) for sector, ticker in sector_etfs.items()}

    print(f"S&P 500 Performance: {sp500_performance:.2f}%")
    print("")
    sorted_sector_performance = sorted(sector_performance.items(), key=lambda item: item[1], reverse=True)
    for sector, performance in sorted_sector_performance:
        print(f"{sector} Performance: {performance:.2f}%")

    outperforming_sectors = {sector: performance for sector, performance in sector_performance.items() if performance > sp500_performance}
    sorted_outperforming_sectors = sorted(outperforming_sectors.items(), key=lambda item: item[1], reverse=True)

    print("")
    print("Sectors outperforming the S&P 500 (sorted from higher to lower performance):")
    for sector, performance in sorted_outperforming_sectors:
        print(f"{sector}: {performance:.2f}%")
    print("")
    print("")

def calculate_sector_dispersion():
    """
    Calculate the dispersion of sector performances using various measures.

    Returns:
    dict: A dictionary containing the range, IQR, variance, and standard deviation of sector performances.
    """
    performances = [__get_performance(ticker) for ticker in sector_etfs.values()]

    dispersion_measures = {
        'Range': np.ptp(performances),
        'IQR (Interquartile Range)': np.percentile(performances, 75) - np.percentile(performances, 25),
        'Variance': np.var(performances),
        'Standard Deviation': np.std(performances)
    }

    print("Sector Performance Dispersion Measures:")
    for measure, value in dispersion_measures.items():
        print(f"{measure}: {value:.2f}")
    print("")
    print("")

def calculate_sector_52_week_diff(threshold=10):
    """
    Calculate the difference between the 52-week high/low and the current price for each sector ETF,
    and identify buy opportunities based on the percentage difference to the 52-week low.

    Parameters:
    threshold (float): The percentage threshold to consider for buy opportunities (default is 10%).

    Returns:
    pd.DataFrame: A DataFrame containing the sector, 52-week high, 52-week low, current price, 
                  difference to 52-week high, difference to 52-week low, percentage differences,
                  and a column indicating buy opportunities.
    """
    data = []

    for sector, ticker in sector_etfs.items():
        high_52_week, low_52_week, current_price = __get_52_week_high_low(ticker)
        diff_to_high = current_price - high_52_week
        diff_to_low = current_price - low_52_week
        pct_diff_to_high = (diff_to_high / high_52_week) * 100
        pct_diff_to_low = (diff_to_low / low_52_week) * 100
        is_buy_opportunity = pct_diff_to_low <= threshold

        data.append({
            'Sector': sector,
            '52-Week High': high_52_week,
            '52-Week Low': low_52_week,
            'Current Price': current_price,
            'Diff to 52-Week High': diff_to_high,
            'Diff to 52-Week Low': diff_to_low,
            'Pct Diff to 52-Week High': pct_diff_to_high,
            'Pct Diff to 52-Week Low': pct_diff_to_low,
            'Buy Opportunity': is_buy_opportunity
        })

    df = pd.DataFrame(data)
    print("Sector 52-Week Differences and Buy Opportunities based on R:R:")
    print(df)
    print("")
    print("")

def print_sp500_reports():
    # Get the current UTC time
    current_utc_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    print("")
    print(f"### S&P 500 {period} Sector Analysis ### - {current_utc_time}")
    print("")
    check_sector_outperformance()
    calculate_sector_dispersion()
    calculate_sp500_sector_std()
    calculate_sector_52_week_diff()
