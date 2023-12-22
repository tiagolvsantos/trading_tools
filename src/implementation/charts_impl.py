from src.implementation.charts import chartpedia

def chart_general_ta_impl(symbol):
    chartpedia.plot_ma_chart(symbol)

def chart_general_ta_mag7_impl():
    lst_mag7 = ["MSFT","META","GOOGL","NVDA","TSLA","AAPL","AMZN"]
    for symbol in lst_mag7:
        chartpedia.plot_ma_chart(symbol)

def chart_asset_profile_impl(symbol):
    chartpedia.plot_asset_profile(symbol)

def chart_cross_asset_correlation_impl():
    chartpedia.plot_cross_asset_correlation()

def chart_sp500_vix_impl():
    chartpedia.plot_sp500_vix_ratio()

def chart_spx_2d_rsi_impl():
    chartpedia.plot_spx_2d_rsi()

def chart_vix_atr_1_impl():
    chartpedia.plot_vix_atr_1()

def chart_futures_curve_impl(symbol):
    chartpedia.plot_futures_curve(symbol)

def chart_binance_symbol_cvd(symbol,interval,to_tail):
    chartpedia.plot_crypto_cvd(symbol,interval,to_tail)

def chart_sr_crypto(symbol):
    chartpedia.plot_sr_crypto(symbol)

def chart_sr_tradefi(symbol):
    chartpedia.plot_sr_tradefi(symbol)

def chart_etf_flows(symbol):
    chartpedia.plot_etf_flows(symbol)

def chart_crypto_fear_greed():
    chartpedia.plot_crypto_fear_greed_index()

def chart_fear_greed():
    chartpedia.plot_fear_greed_index()

def chart_simple_chart(symbol):
    chartpedia.plot_simple_chart(symbol)

def chart_options_data(symbol):
    chartpedia.get_options_chart(symbol)