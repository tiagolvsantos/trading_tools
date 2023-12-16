from src.implementation.crypto import cryptopedia

def plot_binance_flows_for_asset(symbol):
    cryptopedia.get_crypto_order_flow(symbol)

def get_trending_tokens():
    cryptopedia.get_trending_tokens()

def get_companies_holding_crypto(symbol):
    cryptopedia.get_companies_holding_crypto(symbol)