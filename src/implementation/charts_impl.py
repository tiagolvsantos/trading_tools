from src.implementation.charts import chartpedia

def chart_asset_profile(symbol):
    chartpedia.plot_asset_profile(symbol)
    chartpedia.plot_stock_flows(symbol)

def chart_cross_asset_correlation():
    chartpedia.plot_cross_asset_correlation(["ES=F","GC=F","NQ=F","CL=F","DX-Y.NYB","^VIX","^RUT","HG=F","NG=F","RB=F","ZN=F","^STOXX50E","^N225","ZT=F","EURUSD=x","USDJPY=x","HYG","TLT" ,"JNK"], "CrossAsset correlation matrix")

def chart_cross_sector_correlation():
    chartpedia.plot_cross_asset_correlation(["SPY","QQQ","IWM","XLY","XLP","XLE","XLF","XLV","XLI","XLB","XLRE","XLK","XLC","XLU","GDX","GDXJ","MOO","FDN","KIE","KRE","TAN","JETS","IBB","OIH","SMH"], "Sector correlation matrix")

def chart_sp500_vix():
    chartpedia.plot_sp500_vix_ratio()

def chart_vix_atr_1():
    chartpedia.plot_vix_atr_1()

def chart_binance_symbol_cvd(symbol,interval,to_tail):
    chartpedia.plot_crypto_cvd(symbol,interval,to_tail)

def chart_crypto_fear_greed():
    chartpedia.plot_crypto_fear_greed_index()

def chart_fear_greed():
    chartpedia.plot_fear_greed_index()

def chart_options_data(symbol, expiration):
    chartpedia.get_options_chart(symbol, expiration)

def chart_spr():
    chartpedia.plot_spr_chart()

def chart_year_on_year_comparisson(symbol, year):
    chartpedia.chart_year_comparisson_chart(symbol, year)

def chart_skew_sp500():
    chartpedia.chart_skew()

def chart_stock_flows(symbol):
    chartpedia.plot_stock_flows(symbol)

def chart_aaii():
    chartpedia.plot_aaii()

def chart_market_breath(period, indx):
    chartpedia.plot_market_breath(period, indx)

def chart_fast_rsi(symbol):
    chartpedia.plot_chart_rsi_7(symbol)