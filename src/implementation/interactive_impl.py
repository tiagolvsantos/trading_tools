from src.implementation.interactive import bina_ws_agg_trades 
from src.implementation.interactive import bina_abnormal_trading 
from src.implementation.interactive import bitmex_ws_agg_trades


def bina_ws_agg_trades_impl(symbol, threshold ):
    bina_ws_agg_trades.main(symbol,threshold)

def bina_abnormal_trading_impl():
    bina_abnormal_trading.main()

def bitmex_ws_agg_trades_impl(symbol):
    bitmex_ws_agg_trades.main(symbol)