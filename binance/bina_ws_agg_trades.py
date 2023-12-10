import websocket
import json
import typer


class bcolors:
    Red = '\033[91m'
    Green = '\033[92m'

def on_open(ws):
    print(f"Subscribing to Binance trade agg stream for {symbol}...")
    ws.send(json.dumps({
        "method": "SUBSCRIBE",
        "params": [f"{symbol}@aggTrade"],
        "id": 1
    }))

def on_message(ws, message):
    message = json.loads(message)
    side = get_side(message)
    size = message["q"] 
    #print(message)
    if float(size)> 0.1:
        print(f'{bcolors.Red if side == "SELL" else bcolors.Green}{message["s"]} {side} Size:{size} @{message["p"]}')


def on_error(ws, error):
    print("Error occurred:")
    print(error)

def on_close(ws):
    print("WebSocket connection closed.")

def get_side(message):
    if message["m"] == True:
        return "BUY"
    else:
        return "SELL"

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
    main()