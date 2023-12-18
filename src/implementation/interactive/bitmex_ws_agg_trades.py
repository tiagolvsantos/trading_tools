from bitmex_websocket import Instrument
from bitmex_websocket.constants import InstrumentChannels

class bcolors:
    Red = '\033[91m'
    Green = '\033[92m'
    Magenta = '\033[95m'
    Yellow = '\033[93m'
    White = '\33[37m'

def _print_trade(msg):
    print(f'{bcolors.Red if msg["data"][0]["side"] == "Sell" else bcolors.Green}BitMEX | {msg["data"][0]["symbol"]} { msg["data"][0]["side"]} Size: { msg["data"][0]["size"]} @{ msg["data"][0]["price"]}')


def main(symbol):
    channels = [
        InstrumentChannels.trade
    ]

    asset = Instrument(symbol=symbol,
                        channels=channels)
    asset.on('action', lambda msg: _print_trade(msg))

    asset.run_forever()

