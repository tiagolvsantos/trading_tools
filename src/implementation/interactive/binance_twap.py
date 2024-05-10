from binance.client import Client
from datetime import datetime
import os
import time
import numpy as np

class bcolors:
    Red = '\033[91m'
    Green = '\033[92m'
    Magenta = '\033[95m'
    Yellow = '\033[93m'
    White = '\33[37m'
    Reset = '\033[0m'


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

    color = bcolors.Green if prices[-1] > twap else bcolors.Red
    print(f'{color}{dt_string} | {symbol}@{prices[-1]} -> TWAP: {round(twap,2)}{bcolors.Reset}')


def main():
    while True:
        get_binance_twap('BTCUSDT')
        get_binance_twap('ETHUSDT')
        get_binance_twap('SOLUSDT')
        get_binance_twap('BNBUSDT')
        get_binance_twap('ENAUSDT')
        get_binance_twap('WIFUSDT')
        get_binance_twap('DOGEUSDT')
        time.sleep(300) 