from binance.client import Client
from datetime import datetime
import os
import numpy as np

# Initialize the Binance client
client = Client(os.getenv('binance_api_key'), os.getenv('binance_api_secret'))

# Get the historical trades
trades = client.get_historical_trades(symbol='BTCUSDT')

# Calculate the TWAP
prices = np.array([float(trade['price']) for trade in trades])
times = np.array([float(trade['time']) / 1000 for trade in trades])  # Convert to seconds
weights = np.diff(times, prepend=times[0])
twap = np.average(prices, weights=weights)

now = datetime.now()

# Format the date and time
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


print(f'{dt_string} | Last price: {prices[-1]} -> TWAP: {round(twap,2)}')