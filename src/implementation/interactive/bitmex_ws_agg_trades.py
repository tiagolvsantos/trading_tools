# from bitmex_websocket import Instrument
# from bitmex_websocket.constants import InstrumentChannels

# class bcolors:
#     Red = '\033[91m'
#     Green = '\033[92m'
#     Magenta = '\033[95m'
#     Yellow = '\033[93m'
#     White = '\33[37m'

# def _print_trade(msg):
#     global counter_occurence
#     counter_occurence +=1
#     get_position_delta(msg)
#     print(f'{bcolors.Red if msg["data"][0]["side"] == "Sell" else bcolors.Green}BitMEX Perp | {msg["data"][0]["symbol"]} { msg["data"][0]["side"]} Size: { msg["data"][0]["size"]} @{ msg["data"][0]["price"]}')
#     if counter_occurence/occurence == 1:
#         counter_occurence = 0
#         print_position_delta()


# def get_position_delta(msg):
#     global counter_buy 
#     counter_buy += float(msg["data"][0]["price"]) if  msg["data"][0]["side"] == "Buy" else 0
#     global counter_sell 
#     counter_sell += float(msg["data"][0]["price"]) if  msg["data"][0]["side"] == "Sell" else 0

# def print_position_delta():
#     print(f"{bcolors.Yellow}################# POSITION DELTA #################")
#     print(f"{bcolors.Green}Buy: {str(counter_buy)}")
#     print(f"{bcolors.Red}Sell: {str(counter_sell)}")
#     print(f"{bcolors.White}Delta (Buy/Sell): {str(counter_buy / counter_sell)}")
#     print(f"{bcolors.Yellow}##################################################")


# def main(symbol):
#     global counter_buy 
#     counter_buy = 0
#     global counter_sell 
#     counter_sell = 0
#     global counter_occurence
#     counter_occurence = 0
#     global occurence
#     occurence = 500 # configure the number of occurences to print the Delta results

#     channels = [
#         InstrumentChannels.trade
#     ]

#     asset = Instrument(symbol=symbol,
#                         channels=channels)
#     asset.on('action', lambda msg: _print_trade(msg))

#     asset.run_forever()

