from src.libs import openbb_lib
from src.libs import yfinance_lib
from src.libs import technical_indicators_lib
from src.libs import binance_lib
from src.libs import yfinance_lib

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from pylab import rcParams
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pylab import rcParams
import datetime


from statsmodels.tsa.seasonal import seasonal_decompose


def _set_color(x):
    return "red" if (x < 0) else "green"

def _set_markercolor(x):
    return "green" if (x <= 1) else "grey"

def _plot_sr_chart(df_data, symbol, interval):
    df_ppsr = technical_indicators_lib.ppsr(df_data)

    df_ppsr["close"] = pd.to_numeric(df_ppsr["close"])
    df_ppsr["S1"] = pd.to_numeric(df_ppsr["S1"])
    df_ppsr["S2"] = pd.to_numeric(df_ppsr["S2"])
    df_ppsr["S3"] = pd.to_numeric(df_ppsr["S3"])
    df_ppsr["R1"] = pd.to_numeric(df_ppsr["R1"])
    df_ppsr["R2"] = pd.to_numeric(df_ppsr["R2"])
    df_ppsr["R3"] = pd.to_numeric(df_ppsr["R3"])

    print("")
    print(f"# Interval: {interval}")
    print(f"Last quote for {symbol} @ {float(round(df_ppsr['close'].head(1),3))}")
    print (f"Pivot: {float(round(df_ppsr['PP'].head(1),3))} ")
    print (f"R1: {float(round(df_ppsr['R1'].head(1),3))} | S1: {float(round(df_ppsr['S1'].head(1),3))}")
    print (f"R2: {float(round(df_ppsr['R2'].head(1),3))} | S2: {float(round(df_ppsr['S2'].head(1),3))}")
    print (f"R3: {float(round(df_ppsr['R3'].head(1),3))} | S3: {float(round(df_ppsr['S3'].head(1),3))}")

    df_ppsr = df_ppsr.head(7)
    # Plot chart
    fig = go.Figure()

    fig.add_traces([
    go.Candlestick(
        x=df_ppsr["date"],
        open=df_ppsr['open'],
        high=df_ppsr['high'],
        low=df_ppsr['low'],
        close=df_ppsr['close'],
        name= symbol
    ), 
    go.Scatter(
        x=[min(df_ppsr["date"]),max(df_ppsr["date"])],
        y=[float(round(df_ppsr["S1"].head(1),3)),float(round(df_ppsr["S1"].head(1),3))], 
        line={
            'color': 'rgb(50,205,50)',
            'width': 1,
            'dash': 'solid',
        }, name='S1'
    ),
    go.Scatter(
        x=[min(df_ppsr["date"]),max(df_ppsr["date"])],
        y=[float(round(df_ppsr["R1"].head(1),3)),float(round(df_ppsr["R1"].head(1),3))], 
        line={
            'color': 'rgb(240,128,128)',
            'width': 1,
            'dash': 'solid',
        }, name='R1'
    ),  
    go.Scatter(
        x=[min(df_ppsr["date"]),max(df_ppsr["date"])],
        y=[float(round(df_ppsr["S2"].head(1),3)),float(round(df_ppsr["S2"].head(1),3))], 
        line={
            'color': 'rgb(34,139,34)',
            'width': 1,
            'dash': 'solid',
        }, name='S2'
    ), 
    go.Scatter(
        x=[min(df_ppsr["date"]),max(df_ppsr["date"])],
        y=[float(round(df_ppsr["R2"].head(1),3)),float(round(df_ppsr["R2"].head(1),3))], 
        line={
            'color': 'rgb(255,99,71)',
            'width': 1,
            'dash': 'solid',
        }, name='R2'
    ), 
    go.Scatter(
        x=[min(df_ppsr["date"]),max(df_ppsr["date"])],
        y=[float(round(df_ppsr["S3"].head(1),3)),float(round(df_ppsr["S3"].head(1),3))], 
        line={
            'color': 'rgb(46,139,87)',
            'width': 1,
            'dash': 'solid',
        }, name='S3'
    ), 
    go.Scatter(
        x=[min(df_ppsr["date"]),max(df_ppsr["date"])],
        y=[float(round(df_ppsr["R3"].head(1),3)),float(round(df_ppsr["R3"].head(1),3))], 
        line={
            'color': 'rgb(178,34,34)',
            'width': 1,
            'dash': 'solid',
        }, name='R3'
    ), 
    go.Scatter(
        x=[min(df_ppsr["date"]),max(df_ppsr["date"])],
        y=[float(round(df_ppsr["PP"].head(1),3)),float(round(df_ppsr["PP"].head(1),3))], 
        line={
            'color': 'rgb(255,250,205)',
            'width': 1,
            'dash': 'solid',
        }, name='Pivot'
    )
    ])

    # Add figure title
    fig.update_layout(
        title_text=f"{symbol} {interval} S/R Last: {float(round(df_ppsr['close'].head(1),3))} Pivot:{float(round(df_ppsr['PP'].head(1),3))}  R1:{float(round(df_ppsr['R1'].head(1),3))}  S1:{float(round(df_ppsr['S1'].head(1),3))} R2:{float(round(df_ppsr['R2'].head(1),3))} S2:{float(round(df_ppsr['S2'].head(1),3))} R3:{float(round(df_ppsr['R3'].head(1),3))} S3:{float(round(df_ppsr['S3'].head(1),3))} ",
        template="plotly_dark",
        showlegend=True, xaxis_rangeslider_visible=False
    )



    fig.show()

def _plot_crypto_cvd_chart(df_data, symbol, df_oi,to_tail):
    df_data.columns = ['date', 'open', 'high', 'low','close','volume','close time','asset volume', 'number of trades' ,'taker buy asset volume','taker buy quote volume', 'ignore']
    df_cvd = technical_indicators_lib.cumulative_volume_delta(df_data.tail(to_tail))

    fig = make_subplots(rows=4, cols=1)

    fig.append_trace(go.Candlestick(x=df_cvd['date'],
                    open=df_cvd['open'], high=df_cvd['high'],
                    low=df_cvd['low'], close=df_cvd['close'], name = symbol), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=df_cvd['date'],
        y=df_cvd['cumulative_delta'], name = "Delta", line_color='grey',mode='lines',marker = dict(color=list(map(_set_color, df_cvd['delta'])))
    ), row=2, col=1)

    fig.append_trace(go.Scatter(
        x=df_oi['date'],
        y=df_oi['oi'], name = "OI", line_color='#9966CC'
    ), row=3, col=1)

    fig.append_trace(go.Scatter(
        x=df_oi['date'],
        y=df_oi['oi in $'], name = "OI in $", line_color='#682860'
    ), row=4, col=1)


    fig.update_xaxes(rangeslider_visible=False)
    fig.update_layout(title_text=f"{symbol} CVD + OI + OI in $ for {to_tail} Trading periods", template="plotly_dark")
    fig.show()

def plot_ma_chart(symbol:str):
    openbb_lib.plot_ma_asset_chart(symbol, 1440, True)

def plot_asset_profile(symbol:str):
  
    df_data = yfinance_lib.get_symbol_historical_data(symbol)
   
    if len(df_data) < 1:
        print(f"No data for {symbol}")
        return

    df_data["close"] = pd.to_numeric(df_data["close"])
    df_data["volume"] = pd.to_numeric(df_data["volume"])

    df_data = df_data.tail(500)
    df_data_5_trading_years = df_data.tail(2520)
    
    fig = make_subplots(vertical_spacing = 0, rows=3, cols=1, row_heights=[4, 0.2, 2])
    fig.add_trace(go.Candlestick(x=df_data['date'],
                                open=df_data['open'],
                                high=df_data['high'],
                                low=df_data['low'],
                                close=df_data['close']))
    fig.add_trace(go.Histogram(x = df_data["close"], cumulative_enabled = False,  marker_color='#FF9F00'), row=3, col=1)
    fig.add_shape(type="line",
        x0=float(df_data["close"].tail(1)), y0=0, x1=float(df_data["close"].tail(1)), y1=150,
        line=dict(color="Grey",width=3), row=3, col=1
    )
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        xaxis=dict(zerolinecolor='black', showticklabels=False),
        xaxis2=dict(showticklabels=False),
        title_text=f'{symbol} Most traded zones | close: {str(round(float(df_data["close"].tail(1)),3))}',
        template="plotly_dark",
        showlegend=False,
    )

    fig.update_xaxes(title_text = f"Trade data for the close {len(df_data)} trading days".format(), row=3, col=1)
    cs = fig.data[0]

    # Set line and fill colors
    cs.increasing.fillcolor = '#F5F5F5'
    cs.increasing.line.color = '#F5F5F5'
    cs.decreasing.fillcolor = '#FF9F00'
    cs.decreasing.line.color = '#FF9F00'
    fig.show()

    df_data = df_data.set_index('date')
    df_data.index = pd.to_datetime(df_data.index)
    df_data_5_trading_years = df_data_5_trading_years.set_index('date')
    df_data_5_trading_years.index = pd.to_datetime(df_data_5_trading_years.index)

    ## RETURNS
    r = df_data["close"].pct_change()

    rcParams['figure.figsize'] = 20, 10
    Monthly_Returns_List = [
        {
            'Year': r.index[i].year,
            'Month': r.index[i].month,
            'Monthly_Return': r[i],
        }
        for i in range(len(r))
    ]
    Monthly_Returns_List=pd.DataFrame(Monthly_Returns_List,
                                    columns=('Year','Month','Monthly_Return'))
    Monthly_Returns_List["Monthly_Return_perc"] =  Monthly_Returns_List["Monthly_Return"]*100
    Monthly_Returns_List.groupby(['Year', 'Month']).mean()

    Monthly_Returns_List.boxplot(column='Monthly_Return_perc', by='Month', patch_artist = True,
           boxprops = dict(facecolor = "orange"),whiskerprops = dict(color = "orange", linewidth = 1))
    
    ax = plt.gca()
    labels = [item.get_text() for item in ax.get_xticklabels()]
    labels=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

    ax.set_xticklabels(labels)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.title(f"{symbol} Box Plot returns by Month", fontsize=18, fontweight='bold')
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.style.use('dark_background')
    plt.show()



    ## SEASONALITY  
    decomposition = seasonal_decompose(df_data_5_trading_years['close'], model='cummulative', period=30)
    fig = plt.figure()
    fig = decomposition.plot()
    plt.title(f"{symbol} Seasonal decomposition for {len(df_data_5_trading_years)} trading days", fontsize=18, fontweight='bold')
    plt.style.use('dark_background')
    fig.set_size_inches(20, 10)

    seasonality=decomposition.seasonal
    MA1=seasonality.rolling(window=20).mean()
    plt.title(f"{symbol}", fontsize=18, fontweight='bold')
    plt.plot(MA1, label='20D MA')
    plt.title(f"{symbol} Seasonality", fontsize=18, fontweight='bold')
    plt.legend()
    plt.show()

    seasonality=decomposition.seasonal[decomposition.seasonal.index.year == datetime.date.today().year]
    MA1=seasonality.rolling(window=20).mean()
    plt.plot(seasonality, label=f'{symbol}')
    plt.plot(MA1, label='20D MA')
    plt.title(f'{symbol} Seasonality for {datetime.date.today().year}', fontsize=18, fontweight='bold')
    plt.legend()
    plt.show()

def plot_cross_asset_correlation(to_tail=180):
    list_corrs = ["ES=F","GC=F","NQ=F","CL=F","DX-Y.NYB","^VIX","^RUT","HG=F","NG=F","RB=F","ZN=F","^STOXX50E","^N225","ZT=F","EURUSD=x","USDJPY=x","HYG","JNK"]
    df_final = pd.DataFrame()

    for asset in list_corrs:
        df_data = yfinance_lib.get_symbol_historical_data(asset)
        df_data = df_data.tail(to_tail+1).reset_index(drop=True)
        if len(df_data) > int(to_tail):
            df_data['close'] = df_data['close'].astype(float)
            df_data_new = pd.DataFrame(df_data["close"]).rename({'close': asset[0]}, axis=1)
            df_final = pd.concat([df_final, df_data_new.tail(to_tail)], axis=1)

    df_final.columns = ['SP500', 'GOLD', 'NASDAQ100', 'WTI', 'DXY', 'VIX', 'RUSSELL2000', 'COPPER', 'NATGAS', 'RBOB', '10-Year T-Note Futures', 'STOXX50', 'NIKKEI25', '2-Year T-Note Futures',"EURUSD","USDJPY","HYG","JNK"]
    fig = px.imshow(
        df_final.corr(),
        aspect="auto",
        color_continuous_scale="spectral",
        template="plotly_dark",
        title='CrossAsset correlation matrix',
    )
    fig.show()

def plot_sp500_vix_ratio():
    df_spx = yfinance_lib.get_download_data("^GSPC", "1y")
    df_vix = yfinance_lib.get_download_data("^VIX", "1y")

    ratio = (round(df_spx["close"] / df_vix["close"],2)).dropna()
    max_range = df_spx.iloc[len(df_spx)-1]['close'] +   ratio[len(ratio)-30]
    min_range = df_spx.iloc[len(df_spx)-1]['close'] -   ratio[len(ratio)-30]
   
    fig = go.Figure()

    fig.add_traces([
    go.Scatter(
        x=df_spx["date"],
        y=df_spx['close'],
        name= "SP500"
    ), 
    go.Scatter(
        x=[min(df_spx["date"]),max(df_spx["date"])],
        y=[float(max_range),float(max_range)], 
        line={
            'color': 'rgb(153, 0, 0)',
            'width': 1,
            'dash': 'solid',
        }, name= f'Max Range {round(max_range,2)}'
    ), 
    go.Scatter(
        x=[min(df_spx["date"]),max(df_spx["date"])],
        y=[float(min_range),float(min_range)], 
        line={
            'color': 'rgb(0, 102, 0)',
            'width':1,
            'dash': 'solid',
        }, name= f'Min Range {round(min_range,2)}'
    )
    ])

    # Add figure title
    fig.update_layout(
        title_text= f"SP500: {round(df_spx.iloc[len(df_spx)-1]['close'],2)} | VIX: {round(df_vix.iloc[len(df_vix)-1]['close'],2)} | Ratio: {ratio[len(ratio)-1]}  30 days implied range",
        template="plotly_dark",
        showlegend=True,
    )

    fig.show()

def plot_spx_2d_rsi():
    df_spx = yfinance_lib.get_download_data("^GSPC", "1y")
    df_rsi = pd.DataFrame({'rsi':technical_indicators_lib.rsi(df_spx,2)})
    df_spx = pd.concat((df_spx,df_rsi), axis=1)
    
    
    fig = make_subplots(rows=2, cols=1)

    fig.append_trace(go.Candlestick(x=df_spx['date'],
                    open=df_spx['open'], high=df_spx['high'],
                    low=df_spx['low'], close=df_spx['close'], name = "SP500"), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=df_spx['date'],
        y=df_spx['rsi'], name = "2D RSI", line_color='grey',mode='lines'
    ), row=2, col=1)

    fig.add_hrect(y0=0, y1=30, line_width=0, fillcolor="green", opacity=0.2, row=2, col=1)
    fig.add_hrect(y0=80, y1=100, line_width=0, fillcolor="red", opacity=0.2, row=2, col=1)
    fig.update_xaxes(rangeslider_visible=False)
    fig.update_layout(title_text="SP500 2D RSI", template="plotly_dark")
    fig.show()

def plot_vix_atr_1():
    df_vix = yfinance_lib.get_download_data("^VIX", "2y")
    df_spx = yfinance_lib.get_download_data("^GSPC", "2y")
    df_atr = technical_indicators_lib.average_true_range(df_vix,2)

    fig = make_subplots(rows=3, cols=1)

    fig.append_trace(go.Candlestick(x=df_spx['date'],
                    open=df_spx['open'], high=df_spx['high'],
                    low=df_spx['low'], close=df_spx['close'], name = "SPX"), row=1, col=1)
    fig.append_trace(go.Candlestick(x=df_vix['date'],
                    open=df_vix['open'], high=df_vix['high'],
                    low=df_vix['low'], close=df_vix['close'], name = "VIX"), row=2, col=1)

    fig.append_trace(go.Scatter(
        x=df_atr['date'],
        y=df_atr['ATR_2'], name = "VIX ATR", line_color='grey',mode='markers+lines',marker = dict(color=list(map(_set_markercolor, df_atr['ATR_2'])))
    ), row=3, col=1)

    fig.update_xaxes(rangeslider_visible=False)
    fig.update_layout(title_text="SP500 VS VIX ATR < 1 = Brace for impact!", template="plotly_dark")
    fig.show()

def plot_futures_curve(symbol):
    df_data = openbb_lib.get_futures_curve(symbol)
    df_data = df_data.reset_index(drop=False)
    df_data.columns = ['date', 'value']
    fig = px.line(df_data, x="date", y="value", title=f"{symbol} Futures Curve", template="plotly_dark")
    fig.show()

def plot_crypto_cvd(symbol, interval,to_tail):
    try:
        df_data = binance_lib.get_quotes(symbol, interval)
    except Exception:
        return pd.DataFrame()
    
    df_oi = binance_lib.get_open_Interest(symbol, interval)
    df_oi["oi"] = pd.to_numeric(df_oi["oi"])
    df_oi["oi in $"] = pd.to_numeric(df_oi["oi in $"])
    if len(df_data)>0:
        _plot_crypto_cvd_chart(df_data, symbol, df_oi, to_tail)
    else:
        print("NO DATA!")


def _plot_crypto_cvd_chart(df_data, symbol, df_oi,to_tail):
    df_data.columns = ['date', 'open', 'high', 'low','close','volume','close time','asset volume', 'number of trades' ,'taker buy asset volume','taker buy quote volume', 'ignore']
    df_cvd = technical_indicators_lib.cumulative_volume_delta(df_data.tail(to_tail))

    fig = make_subplots(rows=4, cols=1)

    fig.append_trace(go.Candlestick(x=df_cvd['date'],
                    open=df_cvd['open'], high=df_cvd['high'],
                    low=df_cvd['low'], close=df_cvd['close'], name = symbol), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=df_cvd['date'],
        y=df_cvd['cumulative_delta'], name = "Delta", line_color='grey',mode='lines',marker = dict(color=list(map(_set_color, df_cvd['delta'])))
    ), row=2, col=1)

    fig.append_trace(go.Scatter(
        x=df_oi['date'],
        y=df_oi['oi'], name = "OI", line_color='#9966CC'
    ), row=3, col=1)

    fig.append_trace(go.Scatter(
        x=df_oi['date'],
        y=df_oi['oi in $'], name = "OI in $", line_color='#682860'
    ), row=4, col=1)


    fig.update_xaxes(rangeslider_visible=False)
    fig.update_layout(title_text=f"{symbol} CVD + OI + OI in $ for {to_tail} Trading periods", template="plotly_dark")
    fig.show()

def plot_sr_crypto(symbol:str,):
    lst_intervals =["1d","1w","1M"]
    for interval in lst_intervals:
        df_data = binance_lib.get_quotes(symbol, interval)
        if len(df_data) >1:
            df_data.rename(columns = {'open time':'date'}, inplace = True)
        else:
            print("That symbol does not exist!")
        if len(df_data) >1:
            _plot_sr_chart(df_data, symbol, interval)

def plot_sr_tradefi(symbol:str,):
    lst_intervals =["1wk"] # "1d","1wk","1mo"
    for interval in lst_intervals:
        df_data = yfinance_lib.get_download_data(symbol= symbol,interval=interval)

        if len(df_data) >1:
            df_data["open"] = pd.to_numeric(df_data["open"])
            df_data["high"] = pd.to_numeric(df_data["high"])
            df_data["low"] = pd.to_numeric(df_data["low"])
            df_data["close"] = pd.to_numeric(df_data["close"])
        else:
            print("That symbol does not exist!")
        if len(df_data) >1:
            _plot_sr_chart(df_data, symbol, interval)
