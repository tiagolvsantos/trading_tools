import math
from datetime import datetime, timedelta
from threading import Timer
import webbrowser

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf

def _moving_average(df, n):
    MA = pd.Series(df['Close'].rolling(n, min_periods=n).mean(), name=f'MA_{str(n)}')
    return MA

# Create a Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.Label('Enter ticker, separated by commas as per Yahoo Finance {Press Enter}:'),
    dcc.Input(
        id='ticker-input', 
        type='text', 
        value='AAPL,MSFT,GOOGL,AMZN,TSLA,META,NFLX',
        n_submit=0,  # Initialize n_submit to 0
        style={'width': '500px', 'height': '50px'}
    ),
    dcc.Graph(id='live-graph', style={'height': '100%', 'width': '100%'}),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # 60 seconds in milliseconds
        n_intervals=0
    )
], style={'position': 'absolute', 'top': '0', 'left': '0', 'bottom': '0', 'right': '0', 'height': '100vh', 'width': '100%', 'margin': '0', 'padding': '0'})

# Define the callback to update the graph
@app.callback(Output('live-graph', 'figure'),
              Input('ticker-input', 'n_submit'),
              State('ticker-input', 'value'))
def update_graph(n_submit, ticker_input):
    # If the Enter key has not been pressed, return an empty figure
    if n_submit is None:
        return go.Figure()

    # Split the ticker input into a list and convert to uppercase
    list_ticker = [ticker.upper() for ticker in ticker_input.split(',')]

    # Calculate the date 180 days ago
    start = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')

    # Calculate the number of rows and columns for the subplot
    n = len(list_ticker)
    rows = cols = math.ceil(math.sqrt(n))

    # Create subplots with the calculated number of rows and columns
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=list_ticker)

    for i, ticker in enumerate(list_ticker):
        try:
            # Download historical data for desired ticker symbol
            df = yf.download(ticker, start=start, progress=False)
        except KeyError:
            print(f"Could not download data for {ticker}")
            continue
        
        # Calculate 50-day moving average
        df['MA50'] = _moving_average(df, 50)

        # Calculate mean reversion
        mean_reversion = df['Close'].mean()

        # Calculate row and column for subplot
        row = i // cols + 1
        col = i % cols + 1

        # Add a candlestick chart to the subplot
        fig.add_trace(go.Candlestick(x=df.index,
                                    open=df['Open'],
                                    high=df['High'],
                                    low=df['Low'],
                                    close=df['Close'],
                                    name=ticker,
                                    showlegend=False),
                    row=row, col=col)

        # Add 50-day moving average to the subplot
        fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='MA50', line=dict(color='darkmagenta', width=1), showlegend=False), row=row, col=col)

        # Add mean reversion to the subplot
        fig.add_trace(go.Scatter(x=[df.index[0], df.index[-1]], y=[mean_reversion, mean_reversion], name=f'{ticker} Mean Reversion: {mean_reversion:.2f}', line=dict(color='magenta', width=1)), row=row, col=col)

    # Customize layout
    fig.update_layout(
        autosize=True,
        title='',
        template='plotly_dark',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(rangeslider_visible=False)

    return fig

# Run the app
if __name__ == '__main__':
    # Open a web browser
    Timer(1, lambda: webbrowser.open('http://127.0.0.1:8050/')).start()
    # Start the Dash app
    app.run_server(debug=False)
