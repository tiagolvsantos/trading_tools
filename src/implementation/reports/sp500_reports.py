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

def calculate_sp500_ranges_based_on_ytd_vix():
    # Fetch historical VIX data
    vix_data = yf.Ticker("^VIX").history(period=period)  # Adjust period as needed
    vix_data.reset_index(inplace=True)  # Reset index to make 'Date' a column
    vix_data['Date'] = vix_data['Date'].dt.date  # Strip the time component

    # Fetch historical S&P 500 data
    sp500_data = yf.Ticker("^GSPC").history(period=period)  # Adjust period as needed
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
    current_sp500_price = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[0]

    # Calculate potential price ranges
    sp500_ranges['Price_Mean'] = current_sp500_price * (1 + sp500_ranges['mean'])
    sp500_ranges['Price_Std_Dev_Up'] = current_sp500_price * (1 + sp500_ranges['mean'] + sp500_ranges['std'])
    sp500_ranges['Price_Std_Dev_Down'] = current_sp500_price * (1 + sp500_ranges['mean'] - sp500_ranges['std'])

    # Print the ranges
    print("")
    print(f"Current S&P 500 Price: {current_sp500_price:.2f}")
    print(f"S&P 500 Next Moves Based on {period} VIX Levels:")
    print(sp500_ranges[['Price_Mean', 'Price_Std_Dev_Up', 'Price_Std_Dev_Down']])
    print("")

def calculate_daily_sp500_vix_rule_of_16_range():
    # Fetch the latest VIX data
    vix_data = yf.Ticker("^VIX").history(period="1d")
    vix_close = vix_data['Close'].iloc[0]

    # Fetch the latest S&P 500 data
    sp500_data = yf.Ticker("^GSPC").history(period="1d")
    sp500_close = sp500_data['Close'].iloc[0]

    # Define the range high and range low based on VIX close using the Rule of 16
    range_percentage = vix_close / 16 / 100  # Convert VIX close to daily percentage move
    range_high = sp500_close * (1 + range_percentage)
    range_low = sp500_close * (1 - range_percentage)

    # Print the calculated ranges
    print("")
    print("Daily S&P 500 Range Calculation based on VIX rule of 16:")
    print(f"Current S&P 500 Price: {sp500_close:.2f}")
    print(f"VIX Close: {vix_close:.2f}")
    print(f"S&P 500 Daily Range High: {range_high:.2f}")
    print(f"S&P 500 Daily Range Low: {range_low:.2f}")
    print("")

def calculate_seasonal_sp500_range():
    # Fetch historical S&P 500 data for the past 5 years
    sp500_data = yf.Ticker("^GSPC").history(period="5y")
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
    latest_sp500_data = yf.Ticker("^GSPC").history(period="1d")
    sp500_close = latest_sp500_data['Close'].iloc[0]

    # Find the average daily return for today
    today_return = seasonal_returns[(seasonal_returns['Month'] == current_month) & (seasonal_returns['Day'] == current_day)]['Daily_Return'].values

    if len(today_return) == 0:
        print("No historical data available for today's date.")
        return

    # Calculate the range high and range low based on the average daily return
    range_percentage = today_return[0]
    range_high = sp500_close * (1 + range_percentage)
    range_low = sp500_close * (1 - range_percentage)

    # Print the calculated ranges
    print("")
    print("Daily S&P 500 Range Calculation based on Seasonality for the past 5 years:")
    print(f"Current S&P 500 Price: {sp500_close:.2f}")
    print(f"Average Daily Return for {today.strftime('%B %d')}: {range_percentage * 100:.2f}%")
    print(f"S&P 500 Daily Range High: {range_high:.2f}")
    print(f"S&P 500 Daily Range Low: {range_low:.2f}")
    print("")

def calculate_sp500_dxy_correlation():
    # Fetch historical data for the S&P 500 and DXY Dollar Index for the past 5 years
    sp500_data = yf.Ticker("^GSPC").history(period="5y")
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
    sp500_data = yf.Ticker("^GSPC").history(period="5d")
    sp500_close = sp500_data['Close'].iloc[-1]

    dxy_data = yf.Ticker("DX-Y.NYB").history(period="5d")
    dxy_close = dxy_data['Close'].iloc[-1]
    dxy_prev_close = dxy_data['Close'].iloc[-2]

    # Calculate the latest DXY return
    dxy_return = (dxy_close - dxy_prev_close) / dxy_prev_close

    # Get the historical correlation between S&P 500 and DXY
    correlation = calculate_sp500_dxy_correlation()

    # Print the correlation value
    print("Correlation between S&P 500 and DXY Dollar Index:")
    print(f"{correlation:.4f}")
    print("")

    # Estimate the expected daily return for the S&P 500 based on the latest DXY return and the historical correlation
    expected_sp500_return = correlation * dxy_return

    # Calculate the possible S&P 500 levels for the day
    sp500_high = sp500_close * (1 + expected_sp500_return)
    sp500_low = sp500_close * (1 - expected_sp500_return)

    # Print the calculated levels
    print("Possible S&P 500 Levels for the Day based on DXY correlation:")
    print(f"Current S&P 500 Price: {sp500_close:.2f}")
    print(f"Expected Daily Return for S&P 500: {expected_sp500_return * 100:.2f}%")
    print(f"S&P 500 Daily Range High: {sp500_high:.2f}")
    print(f"S&P 500 Daily Range Low: {sp500_low:.2f}")
    print("")

def calculate_sp500_10y_correlation():
    # Fetch historical data for the S&P 500 and US 10-Year Treasury Note Yield for the past 5 years
    sp500_data = yf.Ticker("^GSPC").history(period="5y")
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
    print("Correlation between S&P 500 and US 10-Year Treasury Note Yield:")
    print(f"{correlation:.4f}")
    print("")

    return correlation

def calculate_sp500_levels_based_on_10y():
    # Fetch the latest data for the S&P 500 and US 10-Year Treasury Note Yield, including the previous day
    sp500_data = yf.Ticker("^GSPC").history(period="5d")
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
    sp500_high = sp500_close * (1 + expected_sp500_return)
    sp500_low = sp500_close * (1 - expected_sp500_return)

    # Print the calculated levels
    print("Possible S&P 500 Levels for the Day based on US 10-Year Treasury Note Yield correlation:")
    print(f"Current S&P 500 Price: {sp500_close:.2f}")
    print(f"Expected Daily Return for S&P 500: {expected_sp500_return * 100:.2f}%")
    print(f"S&P 500 Daily Range High: {sp500_high:.2f}")
    print(f"S&P 500 Daily Range Low: {sp500_low:.2f}")
    print("")

def calculate_market_pressure():
    # Fetch the options chain data for SPY
    ticker_options = yf.Ticker("SPY")
    expiration_dates = ticker_options.options

    # Get the current date and the date one month from now
    current_date = datetime.now()
    one_month_later = current_date + timedelta(days=30)

    # Filter expiration dates to be within a month from the current date
    filtered_expirations = [date for date in expiration_dates if current_date <= datetime.strptime(date, '%Y-%m-%d') <= one_month_later]

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
    print("Market Pressure Analysis for SPY Options:")
    print(f"Total Dollar Value of Volume for Calls: ${total_call_volume:,.2f}")
    print(f"Total Dollar Value of Volume for Puts: ${total_put_volume:,.2f}")
    print(f"Market Side Exerting More Pressure: {market_side}")
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
    calculate_sp500_ranges_based_on_ytd_vix()
    calculate_daily_sp500_vix_rule_of_16_range()
    calculate_seasonal_sp500_range()
    calculate_sp500_levels_based_on_dxy()
    calculate_sp500_levels_based_on_10y()
    calculate_market_pressure()
