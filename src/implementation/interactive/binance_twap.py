from binance.client import Client
from datetime import datetime
import os
import time
import numpy as np

# Initialize the Binance client
client = Client(os.getenv('binance_api_key'), os.getenv('binance_api_secret'))

def get_binance_twap(symbol):
    # Get the historical trades
    trades = client.get_historical_trades(symbol=symbol)

    # Calculate the TWAP
    prices = np.array([float(trade['price']) for trade in trades])
    times = np.array([float(trade['time']) / 1000 for trade in trades])  # Convert to seconds
    weights = np.diff(times, prepend=times[0])
    twap = np.average(prices, weights=weights)

    now = datetime.now()

    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")


    print(f'{dt_string} | {symbol}@{prices[-1]} -> TWAP: {round(twap,2)}')


def main():
    while True:
        get_binance_twap('BTCUSDT')
        get_binance_twap('ETHUSDT')
        get_binance_twap('SOLUSDT')
        time.sleep(600) 