import pandas as pd
import yfinance as yf
import numpy as np
import tabulate as tb
from datetime import datetime, timezone, timedelta



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
    'Communication Services': 'XLC',
    'Semiconductors': 'SOXX',
    'Biotechnology': 'IBB',
    'Gold Miners': 'GDX',
    'Oil & Gas Exploration & Production': 'XOP',
    'Homebuilders': 'XHB',
    'Cybersecurity': 'HACK',
    'Agribusiness': 'MOO'
}

period = 'YTD'
asset = "$SPX"
asset_ticker ="^GSPC"
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
    # Dictionary to store standard deviations and ETF tickers
    sector_std = {}

    # Fetch historical data and calculate standard deviation of returns
    for sector, etf in sector_etfs.items():
        data = yf.Ticker(etf).history(period=period)  # Adjust period as needed
        returns = data['Close'].pct_change().dropna()
        sector_std[sector] = (returns.std(), etf)

    # Convert to DataFrame for pretty printing
    sector_std_df = pd.DataFrame.from_dict(sector_std, orient='index', columns=['Standard Deviation', 'ETF'])
    sector_std_df.index.name = 'Sector'
    sector_std_df.reset_index(inplace=True)
    sector_std_df = sector_std_df[['ETF', 'Sector', 'Standard Deviation']]
    sector_std_df = sector_std_df.sort_values(by='Standard Deviation', ascending=False)

    # Prepend $ to ETF tickers
    sector_std_df['ETF'] = sector_std_df['ETF'].apply(lambda x: f'${x}')

    print("Higher standard deviation means higher volatility and risk, while lower standard deviation means lower volatility and risk.")
    print("This information helps investors understand the risk associated with different sectors and make informed investment decisions.")
    print("")
    print(tb.tabulate(sector_std_df, headers='keys', tablefmt='fancy_outline', showindex="never"))
    print("")
    print("")

def check_sector_outperformance():
    """
    Check which sectors are outperforming the S&P 500 using sector ETFs.

    Returns:
    list: A sorted list of sectors that are outperforming the S&P 500, from higher to lower performance.
    """
    sp500_ticker = asset_ticker

    sp500_performance = __get_performance(sp500_ticker)
    sector_performance = {sector: __get_performance(ticker) for sector, ticker in sector_etfs.items()}

    print(f"{asset} Performance: {sp500_performance:.2f}% {period}")
    print("")
    sorted_sector_performance = sorted(sector_performance.items(), key=lambda item: item[1], reverse=True)
    for sector, performance in sorted_sector_performance:
        ticker = sector_etfs[sector]
        print(f"${ticker} {sector} Performance: {performance:.2f}%")

    outperforming_sectors = {sector: (performance, sector_etfs[sector]) for sector, performance in sector_performance.items() if performance > sp500_performance}
    sorted_outperforming_sectors = sorted(outperforming_sectors.items(), key=lambda item: item[1][0], reverse=True)

    print("")
    print("Sectors outperforming the S&P 500 (sorted from higher to lower performance):")
    for sector, (performance, ticker) in sorted_outperforming_sectors:
        print(f"${ticker} {sector}: {performance:.2f}%")
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
            'Ticker': ticker,
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
    # Prepend $ to Ticker values
    df['Ticker'] = df['Ticker'].apply(lambda x: f'${x}')
    print("Sector 52-Week Differences and Buy Opportunities based on R:R:")
    print(tb.tabulate(df, headers='keys', tablefmt='fancy_outline', showindex="never"))
    print("")
    print("")

def calculate_sp500_ranges_based_on_ytd_vix():
    # Fetch historical VIX data
    vix_data = yf.Ticker("^VIX").history(period=period)  # Adjust period as needed
    vix_data.reset_index(inplace=True)  # Reset index to make 'Date' a column
    vix_data['Date'] = vix_data['Date'].dt.date  # Strip the time component

    # Fetch historical S&P 500 data
    sp500_data = yf.Ticker(asset_ticker).history(period=period)  # Adjust period as needed
    sp500_data.reset_index(inplace=True)  # Reset index to make 'Date' a column
    sp500_data['Date'] = sp500_data['Date'].dt.date  # Strip the time component

    # Ensure both datasets have the same frequency and align date ranges
    vix_data = vix_data[['Date', 'Close']].rename(columns={'Close': 'Close_vix'})
    sp500_data = sp500_data[['Date', 'Close']].rename(columns={'Close': 'Close_sp500'})

    # Merge data on Date
    merged_data = pd.merge(vix_data, sp500_data, on='Date', how='inner')
    
    # Calculate daily returns of S&P 500
    merged_data['SP500_Return'] = merged_data['Close_sp500'].pct_change()

    # Drop rows with NaN values in SP500_Return
    merged_data.dropna(subset=['SP500_Return'], inplace=True)

    # Group by VIX levels and calculate mean and std of S&P 500 returns
    vix_bins = [0, 15, 20, 25, 30, 35, 40, 100]
    merged_data['VIX_Level'] = pd.cut(merged_data['Close_vix'], bins=vix_bins)
    sp500_ranges = merged_data.groupby('VIX_Level')['SP500_Return'].agg(['mean', 'std'])

    # Fetch the current S&P 500 price
    current_sp500_price = yf.Ticker(asset_ticker).history(period="1d")['Close'].iloc[0]

    # Calculate potential price ranges
    sp500_ranges['Price_Mean'] = current_sp500_price * (1 + sp500_ranges['mean'])
    sp500_ranges['Price_Std_Dev_Up'] = current_sp500_price * (1 + sp500_ranges['mean'] + sp500_ranges['std'])
    sp500_ranges['Price_Std_Dev_Down'] = current_sp500_price * (1 + sp500_ranges['mean'] - sp500_ranges['std'])

    # Print the ranges
    print("")
    print(f"Current {asset} Price: {current_sp500_price:.2f}")
    print(f"{asset} Next Moves Based on {period} VIX Levels:")
    print(sp500_ranges[['Price_Mean', 'Price_Std_Dev_Up', 'Price_Std_Dev_Down']])
    print("")

def calculate_daily_sp500_vix_rule_of_16_range():
    # Fetch the latest VIX data
    vix_data = yf.Ticker("^VIX").history(period="1d")
    vix_close = vix_data['Close'].iloc[0]

    # Fetch the latest S&P 500 data
    sp500_data = yf.Ticker(asset_ticker).history(period="1d")
    sp500_close = sp500_data['Close'].iloc[0]

    # Define the range high and range low based on VIX close using the Rule of 16
    range_percentage = vix_close / 16 / 100  # Convert VIX close to daily percentage move
    range_high = sp500_close * (1 + range_percentage)
    range_low = sp500_close * (1 - range_percentage)

    # Print the calculated ranges
    print("")
    print(f"Daily {asset} Range Calculation based on VIX rule of 16:")
    print(f"Current {asset} Price: {sp500_close:.2f}")
    print(f"VIX Close: {vix_close:.2f}")
    print(f"{asset} Daily Range High: {range_high:.2f}")
    print(f"{asset} Daily Range Low: {range_low:.2f}")
    print("")

def calculate_seasonal_sp500_range():
    # Fetch historical S&P 500 data for the past 5 years
    sp500_data = yf.Ticker(asset_ticker).history(period="5y")
    sp500_data['Date'] = sp500_data.index

    # Calculate daily percentage change
    sp500_data['Daily_Return'] = sp500_data['Close'].pct_change()

    # Extract month and day from the date
    sp500_data['Month'] = sp500_data['Date'].dt.month
    sp500_data['Day'] = sp500_data['Date'].dt.day

    # Group by month and day to calculate the average daily return
    seasonal_returns = sp500_data.groupby(['Month', 'Day'])['Daily_Return'].mean().reset_index()

    # Get today's month and day
    today = datetime.now()
    current_month = today.month
    current_day = today.day

    # Fetch the latest S&P 500 data
    latest_sp500_data = yf.Ticker(asset_ticker).history(period="1d")
    sp500_close = latest_sp500_data['Close'].iloc[0]

    # Find the average daily return for today
    today_return = seasonal_returns[(seasonal_returns['Month'] == current_month) & (seasonal_returns['Day'] == current_day)]['Daily_Return'].values

    if len(today_return) == 0:
        print("No historical data available for today's date.")
        return

    # Calculate the range high and range low based on the average daily return
    range_percentage = today_return[0]
    if range_percentage >= 0:
        range_high = sp500_close * (1 + range_percentage)
        range_low = sp500_close * (1 - range_percentage)
    else:
        range_high = sp500_close * (1 - range_percentage)
        range_low = sp500_close * (1 + range_percentage)
    # Print the calculated ranges
    print("")
    print(f"Daily S&P 500 Range Calculation based on Seasonality for the past 5 years:")
    print(f"Current {asset} Price: {sp500_close:.2f}")
    print(f"Average Daily Return for {today.strftime('%B %d')}: {range_percentage * 100:.2f}%")
    print(f"{asset} Daily Range High: {range_high:.2f}")
    print(f"{asset} Daily Range Low: {range_low:.2f}")
    print("")

def calculate_sp500_dxy_correlation():
    # Fetch historical data for the S&P 500 and DXY Dollar Index for the past 5 years
    sp500_data = yf.Ticker(asset_ticker).history(period="5y")
    sp500_data.reset_index(inplace=True) 
    sp500_data['Date'] = sp500_data['Date'].dt.date

    dxy_data = yf.Ticker("DX-Y.NYB").history(period="5y")
    dxy_data.reset_index(inplace=True) 
    dxy_data['Date'] = dxy_data['Date'].dt.date

    # Calculate daily returns for both indices
    sp500_data['SP500_Return'] = sp500_data['Close'].pct_change()
    dxy_data['DXY_Return'] = dxy_data['Close'].pct_change()

    # Merge the data on the date
    merged_data = pd.merge(sp500_data[['Date', 'SP500_Return']], dxy_data[['Date', 'DXY_Return']], on='Date')

    # Drop rows with NaN values
    merged_data.dropna(inplace=True)

    # Calculate the correlation between the daily returns of the S&P 500 and the DXY Dollar Index
    correlation = merged_data['SP500_Return'].corr(merged_data['DXY_Return'])

    return correlation

def calculate_sp500_levels_based_on_dxy():
    # Fetch the latest data for the S&P 500 and DXY Dollar Index, including the previous day
    sp500_data = yf.Ticker(asset_ticker).history(period="5d")
    sp500_close = sp500_data['Close'].iloc[-1]

    dxy_data = yf.Ticker("DX-Y.NYB").history(period="5d")
    dxy_close = dxy_data['Close'].iloc[-1]
    dxy_prev_close = dxy_data['Close'].iloc[-2]

    # Calculate the latest DXY return
    dxy_return = (dxy_close - dxy_prev_close) / dxy_prev_close

    # Get the historical correlation between S&P 500 and DXY
    correlation = calculate_sp500_dxy_correlation()

    # Print the correlation value
    print(f"Correlation between {asset} and DXY Dollar Index:")
    print(f"{correlation:.4f}")
    print("")

    # Estimate the expected daily return for the S&P 500 based on the latest DXY return and the historical correlation
    expected_sp500_return = correlation * dxy_return

    # Calculate the possible S&P 500 levels for the day
    if expected_sp500_return >= 0:
        sp500_high = sp500_close * (1 + expected_sp500_return)
        sp500_low = sp500_close * (1 - expected_sp500_return)
    else:
        sp500_high = sp500_close * (1 - expected_sp500_return)
        sp500_low = sp500_close * (1 + expected_sp500_return)

    # Print the calculated levels
    print(f"Possible {asset} Levels for the Day based on DXY correlation:")
    print(f"Current {asset} Price: {sp500_close:.2f}")
    print(f"Expected Daily Return for {asset}: {expected_sp500_return * 100:.2f}%")
    print(f"{asset} Daily Range High: {sp500_high:.2f}")
    print(f"{asset} Daily Range Low: {sp500_low:.2f}")
    print("")

def calculate_sp500_10y_correlation():
    # Fetch historical data for the S&P 500 and US 10-Year Treasury Note Yield for the past 5 years
    sp500_data = yf.Ticker(asset_ticker).history(period="5y")
    sp500_data.reset_index(inplace=True) 
    sp500_data['Date'] = sp500_data['Date'].dt.date

    us10y_data = yf.Ticker("^TNX").history(period="5y")
    us10y_data.reset_index(inplace=True) 
    us10y_data['Date'] = us10y_data['Date'].dt.date

    # Calculate daily returns for both indices
    sp500_data['SP500_Return'] = sp500_data['Close'].pct_change()
    us10y_data['US10Y_Return'] = us10y_data['Close'].pct_change()

    # Merge the data on the date
    merged_data = pd.merge(sp500_data[['Date', 'SP500_Return']], us10y_data[['Date', 'US10Y_Return']], on='Date')

    # Drop rows with NaN values
    merged_data.dropna(inplace=True)

    # Calculate the correlation between the daily returns of the S&P 500 and the US 10-Year Treasury Note Yield
    correlation = merged_data['SP500_Return'].corr(merged_data['US10Y_Return'])

    # Print the correlation value
    print(f"Correlation between S&P 500 and US 10-Year Treasury Note Yield:")
    print(f"{correlation:.4f}")
    print("")

    return correlation

def calculate_sp500_levels_based_on_10y():
    # Fetch the latest data for the S&P 500 and US 10-Year Treasury Note Yield, including the previous day
    sp500_data = yf.Ticker(asset_ticker).history(period="5d")
    sp500_close = sp500_data['Close'].iloc[-1]

    us10y_data = yf.Ticker("^TNX").history(period="5d")
    us10y_close = us10y_data['Close'].iloc[-1]
    us10y_prev_close = us10y_data['Close'].iloc[-2]

    # Calculate the latest US 10-Year Treasury Note Yield return
    us10y_return = (us10y_close - us10y_prev_close) / us10y_prev_close

    # Get the historical correlation between S&P 500 and US 10-Year Treasury Note Yield
    correlation = calculate_sp500_10y_correlation()

    # Estimate the expected daily return for the S&P 500 based on the latest US 10-Year Treasury Note Yield return and the historical correlation
    expected_sp500_return = correlation * us10y_return

    # Calculate the possible S&P 500 levels for the day
    if expected_sp500_return >= 0:
        sp500_high = sp500_close * (1 + expected_sp500_return)
        sp500_low = sp500_close * (1 - expected_sp500_return)
    else:
        sp500_high = sp500_close * (1 - expected_sp500_return)
        sp500_low = sp500_close * (1 + expected_sp500_return)

    # Print the calculated levels
    print(f"Possible {asset} Levels for the Day based on US 10-Year Treasury Note Yield correlation:")
    print(f"Current {asset} Price: {sp500_close:.2f}")
    print(f"Expected Daily Return for {asset}: {expected_sp500_return * 100:.2f}%")
    print(f"{asset} Daily Range High: {sp500_high:.2f}")
    print(f"{asset} Daily Range Low: {sp500_low:.2f}")
    print("")

def calculate_market_pressure():
    # Fetch the options chain data for SPY
    ticker_options = yf.Ticker("SPY")
    expiration_dates = ticker_options.options

    # Get the current date and the date one month from now
    current_date = datetime.now()
    diff_days = current_date + timedelta(days=5)

    # Filter expiration dates to be within a month from the current date
    filtered_expirations = [date for date in expiration_dates if current_date <= datetime.strptime(date, '%Y-%m-%d') <= diff_days]

    # Get the nearest expiration date within the filtered expirations
    nearest_expiration = filtered_expirations[0]

    # Fetch the options chain for the nearest expiration date
    options = ticker_options.option_chain(nearest_expiration)

    # Combine calls and puts data
    calls = options.calls
    puts = options.puts

    # Calculate the total dollar value of open interest at each strike price for calls and puts
    calls['Total_Call_Volume'] = calls['volume'] * calls['strike']
    puts['Total_Put_Volume'] = puts['volume'] * puts['strike']

    # Sum the total dollar value of open interest for calls and puts
    total_call_volume = calls['Total_Call_Volume'].sum()
    total_put_volume = puts['Total_Put_Volume'].sum()

    # Determine which side is exerting more pressure
    if total_call_volume > total_put_volume:
        market_side = "Calls"
    else:
        market_side = "Puts"

    # Print the total dollar value of open interest for calls and puts, and the market side
    print("")
    print("Daily Market Pressure Analysis for $SPY Options:")
    print(f"Total Dollar Value of Volume for Calls: ${total_call_volume:,.2f}")
    print(f"Total Dollar Value of Volume for Puts: ${total_put_volume:,.2f}")
    print(f"Market Side Exerting More Pressure: {market_side}")
    print("")

def calculate_mag7_weight_on_sp500():
    # Define the MAG 7 stocks
    mag7_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"]

    # Fetch historical data for the S&P 500 and MAG 7 stocks for the past year
    sp500_data = yf.Ticker(asset_ticker).history(period="1y")
    sp500_data.reset_index(inplace=True)  # Reset index to make 'Date' a column

    mag7_data = {ticker: yf.Ticker(ticker).history(period="1y").reset_index() for ticker in mag7_tickers}

    # Calculate daily returns for the S&P 500
    sp500_data['SP500_Return'] = sp500_data['Close'].pct_change()

    # Calculate daily returns for each of the MAG 7 stocks
    for ticker in mag7_tickers:
        mag7_data[ticker]['Return'] = mag7_data[ticker]['Close'].pct_change()

    # Fetch the latest market capitalization for each of the MAG 7 stocks
    mag7_market_caps = {ticker: yf.Ticker(ticker).info['marketCap'] for ticker in mag7_tickers}

    # Calculate the total market capitalization of the MAG 7 stocks
    total_market_cap = sum(mag7_market_caps.values())

    # Calculate the weighted average return of the MAG 7 stocks
    weighted_returns = pd.DataFrame()
    for ticker in mag7_tickers:
        weight = mag7_market_caps[ticker] / total_market_cap
        weighted_returns[ticker] = mag7_data[ticker]['Return'] * weight

    weighted_avg_return = weighted_returns.sum(axis=1)

    # Merge the S&P 500 returns with the weighted average return of the MAG 7 stocks
    merged_data = pd.DataFrame({
        'SP500_Return': sp500_data['SP500_Return'],
        'MAG7_Weighted_Return': weighted_avg_return
    }).dropna()

    # Calculate the correlation between the S&P 500 return and the weighted average return of the MAG 7 stocks
    correlation = merged_data['SP500_Return'].corr(merged_data['MAG7_Weighted_Return'])

    # Print the correlation value
    print(f"Correlation between {asset} and MAG 7 Weighted Average Return:")
    print(f"{correlation:.4f}")
    print("")

    # Print the daily performance for the last day for the MAG 7 stocks in percentage
    print("Daily Performance for the MAG 7 Stocks (Last Day):")
    for ticker in mag7_tickers:
        last_return = mag7_data[ticker]['Return'].dropna().iloc[-1] * 100  # Get the last available return and convert to percentage
        print(f"${ticker} Last Day Return: {last_return:.2f}%")
    print("")

def classify_risk_regime():
    # Fetch historical data for the S&P 500 and VIX for the past year
    sp500_data = yf.Ticker(asset_ticker).history(period="1y")
    vix_data = yf.Ticker("^VIX").history(period="1y")

    # Calculate the 50-day and 200-day moving averages for the S&P 500
    sp500_data['50_MA'] = sp500_data['Close'].rolling(window=50).mean()
    sp500_data['200_MA'] = sp500_data['Close'].rolling(window=200).mean()

    # Determine the market structure based on moving averages
    sp500_data['Market_Structure'] = sp500_data['50_MA'] > sp500_data['200_MA']

    # Determine the current market structure
    current_market_structure = sp500_data['Market_Structure'].iloc[-1]

    # Determine the current volatility level based on the VIX
    current_vix = vix_data['Close'].iloc[-1]

    # Define thresholds for high, medium, and low volatility
    high_volatility_threshold = 20  # Example threshold for high volatility
    low_volatility_threshold = 15   # Example threshold for low volatility

    # Classify the regime based on market structure and volatility
    if current_market_structure:
        if current_vix < low_volatility_threshold:
            regime = "Risk-On"
        elif current_vix < high_volatility_threshold:
            regime = "Neutral"
        else:
            regime = "Risk-Off"
    else:
        if current_vix < low_volatility_threshold:
            regime = "Neutral"
        else:
            regime = "Risk-Off"

    # Print the classification
    print("")
    print("Current Market Regime Classification:")
    print(f"Market Structure (50_MA > 200_MA): {current_market_structure}")
    print(f"Current $VIX Level: {current_vix:.2f}")
    print(f"Regime: {regime}")
    print("")

def calculate_sp500_relative_impact():
    # Fetch the list of S&P 500 stocks
    sp500_symbols = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()

   # Replace '.' with '-' in the symbols
    sp500_symbols = [symbol.replace('.', '-') for symbol in sp500_symbols]

    # Retrieve market cap and performance data for each stock
    stocks_data = []
    for symbol in sp500_symbols:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        history = ticker.history(period=period)
        if not history.empty:
            performance = (history['Close'][-1] - history['Close'][0]) / history['Close'][0] * 100
            stocks_data.append({
                'symbol': symbol,
                'market_cap': info.get('marketCap', 0),
                'performance': performance
            })

    # Convert to DataFrame
    df = pd.DataFrame(stocks_data)

    # Filter out stocks with missing market cap
    df = df[df['market_cap'] > 0]

    # Calculate the relative impact on performance by market cap
    total_market_cap = df['market_cap'].sum()
    df['relative_impact'] = df['market_cap'] / total_market_cap * df['performance']

    # Sort by relative impact
    df_sorted = df.sort_values(by='relative_impact', ascending=False)

    # sort performance and relative impact columns
    df_sorted['performance'] = df_sorted['performance'].apply(lambda x: f"{x:.2f}%")
    df_sorted['relative_impact'] = df_sorted['relative_impact'].apply(lambda x: f"{x:.2f}%")

    # Separate into two DataFrames
    df_top_positive = df_sorted.head(5).sort_values(by='relative_impact', ascending=False)
    df_top_positive['symbol'] = df_top_positive['symbol'].apply(lambda x: f"${x}")

    df_top_negative = df_sorted.tail(5).sort_values(by='relative_impact', ascending=True)
    df_top_negative['symbol'] = df_top_negative['symbol'].apply(lambda x: f"${x}")

    # General statistics
    positive_impact_stocks = df_sorted[df_sorted['relative_impact'].str.rstrip('%').astype(float) > 0]
    negative_impact_stocks = df_sorted[df_sorted['relative_impact'].str.rstrip('%').astype(float) < 0]

    print("Summary Statistics:")
    print(f"Number of stocks with positive impact: {len(positive_impact_stocks)}")
    print(f"Number of stocks with negative impact: {len(negative_impact_stocks)}")

    average_performance_positive = positive_impact_stocks['performance'].str.rstrip('%').astype(float).mean()
    average_performance_negative = negative_impact_stocks['performance'].str.rstrip('%').astype(float).mean()

    print(f"Average performance for positive impact stocks: {average_performance_positive:.2f}%")
    print(f"Average performance for negative impact stocks: {average_performance_negative:.2f}%")

    # Print specific statistics for performance and relative impact
    print("\nPerformance Statistics:")
    print(f"Mean: {df_sorted['performance'].str.rstrip('%').astype(float).mean():.2f}%")
    print(f"Median: {df_sorted['performance'].str.rstrip('%').astype(float).median():.2f}%")
    print(f"Standard Deviation: {df_sorted['performance'].str.rstrip('%').astype(float).std():.2f}%")

    print("\nRelative Impact Statistics:")
    print(f"Mean: {df_sorted['relative_impact'].str.rstrip('%').astype(float).mean():.2f}%")
    print(f"Median: {df_sorted['relative_impact'].str.rstrip('%').astype(float).median():.2f}%")
    print(f"Standard Deviation: {df_sorted['relative_impact'].str.rstrip('%').astype(float).std():.2f}%")

    # Print top 5 positive and negative relative impact
    print("\nTop 5 Positive Relative Impact:")
    print(tb.tabulate(df_top_positive, headers='keys', tablefmt='fancy_outline', showindex="never"))
    print("\nTop 5 Negative Relative Impact:")
    print(tb.tabulate(df_top_negative, headers='keys', tablefmt='fancy_outline', showindex="never"))







def print_sp500_reports():
    # Get the current UTC time
    current_utc_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    print("")
    print(f"### {asset} {period} Sector Analysis ### - {current_utc_time}")
    print("")
    check_sector_outperformance()
    calculate_sector_dispersion()
    calculate_sp500_sector_std()
    calculate_sector_52_week_diff()
    calculate_mag7_weight_on_sp500()
    print("### SP500 Price Ranges ###")
    calculate_sp500_ranges_based_on_ytd_vix()
    calculate_daily_sp500_vix_rule_of_16_range()
    calculate_seasonal_sp500_range()
    calculate_sp500_levels_based_on_dxy()
    calculate_sp500_levels_based_on_10y()
    print("### Market Signals ###")
    calculate_market_pressure()
    classify_risk_regime()
    calculate_sp500_relative_impact()


