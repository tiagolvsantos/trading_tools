import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import src.libs.utils as utils
import warnings
import src.libs.binance_lib as binance_lib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
warnings.filterwarnings("ignore")


def _dispersion_chart(data, ax):
    sns.scatterplot(x="price", y="quantity", hue="side", data=data, ax=ax)
    ax.set_xlabel("Price")
    ax.set_ylabel("Quantity")
    plt.show(block=True)

def _bar_chart(arg0, arg1, symbol):
    # Book Dispersion
    fig, result = plt.subplots()
    plt.style.use(arg0)
    result.set_title(f"{arg1}{symbol}")
    return result

def _plot_heatmap_price(symbol:str, df_data):
    # Load the order book data into a Pandas DataFrame
    # Create a pivot table with the bids and asks as the columns and the price levels as the index
    pivot = df_data.pivot_table(index="price", values="quantity")

    # Create the heatmap trace
    trace = go.Heatmap(x=pivot.columns, y=pivot.index, z=pivot.values, colorscale='YlGnBu')

    # Create the figure
    fig = go.Figure(data=[trace])
    fig['layout'].update(plot_bgcolor='black')

    # Display the figure
    fig.show()

def _plot_summary(symbol, df_data):
    fig = go.Figure()

    ax = _bar_chart(
        'dark_background', 'BOOK DISPERSION CHART ', symbol
    )
    sns.scatterplot(x="price", y="quantity", hue="side", data=df_data, ax=ax)
    plt.show(block=True)

    ax = _bar_chart(
        'dark_background', 'BOOK ORDER RANGE ', symbol
    )
    sns.histplot(x="price", hue="side", data=df_data, ax=ax)
    sns.rugplot(x="price", hue="side", data=df_data, ax=ax)
    plt.show(block=True)

    ax = _bar_chart(
        'dark_background',
        'BOOK DISPERSION CHART WEIGHTED BY QUANTITY OF ORDERS ',
        symbol,
    )
    sns.histplot(x="price", weights="quantity", hue="side", data=df_data, ax=ax)
    _dispersion_chart(df_data, ax)
    ax = _bar_chart(
        'grayscale', 'BOOK ORDER DEPTH CHART ', symbol
    )
    sns.ecdfplot(x="price", weights="quantity", stat="count", complementary=True, data=df_data[df_data['side'] =="bids"], ax=ax)
    sns.ecdfplot(x="price", weights="quantity", stat="count", data=df_data[df_data['side'] =="asks"], ax=ax)
    _dispersion_chart(df_data, ax)


def get_crypto_order_flow(symbol:str):

    df_data = binance_lib.get_order_book_depth(symbol)

    # BID ASK RATIO  ranges from -1 to 1.
    # The ratio essentially shows which side is stronger and by how much. So let's say bids = 5million and asks = 2.5million. bid ask ratio = (5 - 2.5) / (5 + 2.5) = 0.33. --> implying, more demand than supply.

    bid_total = 0
    ask_total = 0
    for  index, row in df_data.iterrows():
        if row["side"] == "asks":
            ask_total+= row["price"] * row["quantity"]
        if row["side"] == "bids":
            bid_total+= row["price"] * row["quantity"]
    
    bid_ask_ratio = (bid_total - ask_total) / (bid_total + ask_total)

    print("If the ratio is 1, it means 100% demand and no supply. For example, if bids = 1million and asks = 0.")
    print("If the ratio is -1, it means 100% supply and no demand. For example, if asks = 1million and bids = 0.")
    print("If the ratio is 0, it means supply and demand are equal. For example, if asks = 1million and bids = 1million.")
    print("")
    print(f"Current bid/ask ratio for {symbol} is {round(bid_ask_ratio,3)}")
    print(f"Total Bids in ${utils.print_formated_numbers(round(bid_total,3))}")
    print(f"Total Asks in ${utils.print_formated_numbers(round(ask_total,3))}")
    print("")

    # Book Summary
    price_summary = df_data.groupby("side").price.describe()
    print(f"PRICE SUMMARY FOR {symbol}")
    print(price_summary)
    print()

    r = requests.get("https://api.binance.com/api/v3/ticker/bookTicker", params=dict(symbol=symbol))
    book_top = r.json()
    name = book_top.pop("symbol")  # get symbol and also delete at the same time
    s = pd.Series(book_top, name=name, dtype=float)

    # Print Book Status
    print(f"ORDER BOOK STATUS FOR {symbol}")
    for i,r in s.items():
        print(i,r)

    _plot_summary(symbol, df_data)

def plot_aggtrades(symbol:str):
    df_data = binance_lib.get_daily_aggtrades(symbol)
    fig = go.Figure(data=go.Heatmap(
            z=df_data["qty"],
            x=df_data["price"],
            y=df_data["date"],
            colorscale='Viridis'))

    fig.update_layout(
        title='GitHub commits per day')

    fig.show()

def plot_net_asset_taker(symbol:str):
    df_data = binance_lib.get_quotes(symbol)
    df_data["Net taker volume"] = pd.to_numeric(df_data["asset volume"]) - pd.to_numeric(df_data["taker buy quote volume"])

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=pd.to_datetime(df_data["open time"]), y=pd.to_numeric(df_data["close"]), name="Price"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=pd.to_datetime(df_data["open time"]), y=pd.to_numeric(df_data["Net taker volume"]), name="Taker"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text=f"{symbol} Net asset taker volume vs price",
        template="plotly_dark",
        showlegend=True,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="By calculating the 'Net Taker Volume' for each date and then visualizing it on the Bitcoin chart, it is evident that the indicator is a good counter indicator for the price of Bitcoin. <br>"+
                        "― If the price of Bitcoin is high, but aggressive selling is taking place, it is clear that the top is near. <br>" + "― If the price of Bitcoin is low, and aggressive buying is taking place, it is clear that there is a bottom.")

    # Set y-axes titles
    fig.update_yaxes(title_text=f"<b>{symbol}</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Net asset taker volume</b>e", secondary_y=True)

    fig.show()