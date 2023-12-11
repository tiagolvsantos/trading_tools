from src.implementation.interactive import bina_ws_agg_trades 
from src.implementation.interactive import bina_abnormal_trading 


def bina_ws_agg_trades_impl(symbol, threshold ):
    bina_ws_agg_trades.main(symbol,threshold)

def bina_abnormal_trading_impl():
    bina_abnormal_trading.main()
