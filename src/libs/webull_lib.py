from webull import webull

# init webull object
wb = webull()

def get_quote(symbol: str):
    data = wb.get_quote(symbol)
    if len(data)> 1:
        return data
    else:
        {}

def get_analysis(symbol: str):
    data = wb.get_analysis(symbol)
    if len(data)> 1:
        return data
    else:
        {}

def get_options(symbol: str):
    data = wb.get_options(symbol)
    if len(data)> 1:
        return data
    else:
        {}

# wb.get_options_by_strike_and_expire_date('AAPL', '2022-03-18', '70')
def get_options_by_strike_and_expire_date(symbol: str, expiration_date: str, strike:str):
    data = wb.get_options_by_strike_and_expire_date(symbol, expiration_date, strike)
    if len(data)> 1:
        return data
    else:
        {}

'''
add price/percent/volume alert
frequency: 1 is once a day, 2 is once a minute
interval: 1 is once, 0 is repeating
priceRules: list of dicts with below attributes per alert
    field: price , percent , volume
    type: price (above/below), percent (above/below), volume (vol in thousands)
    value: price, percent, volume amount
    remark: comment
rules example:
priceRules = [{'field': 'price', 'type': 'above', 'value': '900.00', 'remark': 'above'}, {'field': 'price', 'type': 'below',
        'value': '900.00', 'remark': 'below'}]
smartRules = [{'type':'earnPre','active':'on'},{'type':'fastUp','active':'on'},{'type':'fastDown','active':'on'},
    {'type':'week52Up','active':'on'},{'type':'week52Down','active':'on'},{'type':'day5Down','active':'on'}]
price_rules = [{'field': 'price', 'type': 'above', 'value': '900.00', 'remark': 'above'}, {'field': 'price', 'type': 'below','value': '900.00', 'remark': 'below'}]
smart_rules = [{'type':'earnPre','active':'on'},{'type':'fastUp','active':'on'},{'type':'fastDown','active':'on'},{'type':'week52Up','active':'on'},{'type':'week52Down','active':'on'},{'type':'day5Down','active':'on'}]
'''
def alerts_add(symbol: str, frequency: str, interval:str, price_rules: list, smart_rules: list):
    data = wb.alerts_add(symbol, frequency, interval, price_rules ,smart_rules)
    if len(data)> 1:
        return data
    else:
        {}

def active_gainer_loser():
    data = wb.active_gainer_loser()
    if len(data)> 1:
        return data
    else:
        {}

'''
Notice the fact that endpoints are reversed on lte and gte, but this function makes it work correctly
Also screeners are not sent by name, just the parameters are sent
example: run_screener( price_lte=.10, price_gte=5, pct_chg_lte=.035, pct_chg_gte=.51)
just a start, add more as you need it
'''
def run_screener(region=None, price_lte=None, price_gte=None, pct_chg_gte=None, pct_chg_lte=None, sort=None,
                     sort_dir=None, vol_lte=None, vol_gte=None):
    data = wb.run_screener(region, price_lte, price_gte, pct_chg_gte, pct_chg_lte, sort,
                     sort_dir, vol_lte, vol_gte)
    if len(data)> 1:
        return data
    else:
        {}

def get_capital_flow(symbol: str):
    data = wb.get_capital_flow(symbol)
    if len(data)> 1:
        return data
    else:
        {}

def get_etf_holding(symbol: str):
    data = wb.get_etf_holding(symbol)
    if len(data)> 1:
        return data
    else:
        {}

def get_institutional_holding(symbol: str):
    data = wb.get_institutional_holding(symbol)
    if len(data)> 1:
        return data
    else:
        {}

def get_short_interest(symbol: str):
    data = wb.get_short_interest(symbol)
    if len(data)> 1:
        return data
    else:
        {}

def get_financials(symbol: str):
    data = wb.get_financials(symbol)
    if len(data)> 1:
        return data
    else:
        {}

def get_news(symbol: str):
    data = wb.get_news(symbol)
    if len(data)> 1:
        return data
    else:
        {}

def get_calendar(symbol: str):
    data = wb.get_calendar(symbol)
    if len(data)> 1:
        return data
    else:
        {}

def get_five_min_ranking():
    data = wb.get_five_min_ranking()
    if len(data)> 1:
        return data
    else:
        {}

'''
get bars returns a pandas dataframe
params:
    interval: m1, m5, m15, m30, h1, h2, h4, d1, w1
    count: number of bars to return
    extendTrading: change to 1 for pre-market and afterhours bars
    timeStamp: If epoc timestamp is provided, return bar count up to timestamp. If not set default to current time.
    stock=None, tId=None, interval='m1', count=1, extendTrading=0, timeStamp=None
'''
def get_bars(symbol: str, interval: str):
    data = wb.get_bars(symbol, interval)
    if len(data)> 1:
        return data
    else:
        {}

def get_bars_crypto(symbol: str, interval: str):
    data = wb.get_bars_crypto(symbol, interval)
    if len(data)> 1:
        return data
    else:
        {}

'''
get bars returns a pandas dataframe
params:
    derivativeId: to be obtained from option chain, eg option_chain[0]['call']['tickerId']
    interval: 1m, 5m, 30m, 60m, 1d
    count: number of bars to return
    direction: 1 ignores {count} parameter & returns all bars on and after timestamp
                setting any other value will ignore timestamp & return latest {count} bars
    timeStamp: If epoc timestamp is provided, return bar count up to timestamp. If not set default to current time.
    derivativeId=None, interval='1m', count=1, direction=1, timeStamp=None)
'''
def get_options_bars(symbol: str, interval: str):
    data = wb.get_options_bars(symbol, interval)
    if len(data)> 1:
        return data
    else:
        {}