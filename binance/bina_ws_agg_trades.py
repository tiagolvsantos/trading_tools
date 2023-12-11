import websocket
import json
import typer


class bcolors:
    Red = '\033[91m'
    Green = '\033[92m'
    Magenta = '\033[95m'
    Yellow = '\033[93m'
    White = '\33[37m'

def on_open(ws):
    print(f"{bcolors.White}Subscribing to Binance trade agg stream for {symbol}...")
    ws.send(json.dumps({
        "method": "SUBSCRIBE",
        "params": [f"{symbol}@aggTrade"],
        "id": 1
    }))

def on_message(ws, message):
    message = json.loads(message)
    side = get_side(message)
    size = message["q"]
    global counter_occurence 
    counter_occurence +=1
    global occurence
    
    get_position_delta(message,side)
    if float(size)> float(threshold):
        print(f'{bcolors.Red if side == "SELL" else bcolors.Green}{message["s"]} {side} Size:{size} @{message["p"]}')
    

    if counter_occurence/occurence == 1:
        counter_occurence = 0
        print_position_delta()


def on_error(ws, error):
    print(f"{bcolors.White}Error occurred:")
    print(error)

def on_close(ws):
    print(f"{bcolors.White}WebSocket connection closed.")

def get_side(message):
    return "BUY" if message["m"] == True else "SELL"

def get_position_delta(message, side):
    global counter_buy 
    counter_buy += float(message["q"]) if  side == "BUY" else 0
    global counter_sell 
    counter_sell += float(message["q"]) if  side == "SELL" else 0

def print_position_delta():
    print(f"{bcolors.Yellow}#################### POSITION DELTA ####################")
    print(f"{bcolors.Green}Buy: {str(counter_buy)}")
    print(f"{bcolors.Red}Sell: {str(counter_sell)}")
    print(f"{bcolors.White}Delta (Buy/Sell): {str(counter_buy / counter_sell)}")
    print(f"{bcolors.Yellow}########################################################")


def main():
    socket = "wss://stream.binance.com:9443/ws"
    ws = websocket.WebSocketApp(socket,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

    ws.run_forever()

if __name__ == "__main__":
    symbol = input("Select a symbol:")
    threshold = input("Select a threshold:")
   
    counter_sell = 0
    counter_buy = 0
    counter_occurence = 0
    occurence = 1000 # configure the number of occurences to print the Delta results
    main()