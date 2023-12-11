import os

def configure_env_vars():
    if "QUANDL_AUTH" not in os.environ:
        os.environ["QUANDL_AUTH"] = ""
    if "FINNHUB_KEY" not in os.environ:
        os.environ["FINNHUB_KEY"] = ""
    if "FINANCIALMODELINGPREP" not in os.environ:
        os.environ["FINANCIALMODELINGPREP"] = ""
    if "FRED" not in os.environ:
        os.environ["FRED"] = ""
    if "ALPHAVANTAGE" not in os.environ:
        os.environ["ALPHAVANTAGE"] = ""