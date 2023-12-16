import requests
import json
import locale 


class Token:
  def __init__(self, query_json:json):
    self.Name = query_json["item"]["name"]
    self.symbol = query_json["item"]["symbol"]
    self.price = query_json["item"]["data"]["price"]
    self.percentage_change = f'{round(float(query_json["item"]["data"]["price_change_percentage_24h"]["usd"]),2)}%'
    self.total_volume = query_json["item"]["data"]["total_volume"]
    self.market_cap = query_json["item"]["data"]["market_cap"]

class Company:
  def __init__(self, query_json:json):
    self.Name = query_json["name"]
    self.symbol = query_json["symbol"]
    self.total_holdings = query_json["total_holdings"]
    self.entry_value = locale.currency(query_json["total_entry_value_usd"], grouping=True)
    self.current_value_usd = locale.currency(query_json["total_current_value_usd"], grouping=True)

def get_trending_coins():
    url = "https://api.coingecko.com/api/v3/search/trending"
    try:
        list_coins = requests.get(url).json()["coins"]
        return [Token(record).__dict__ for record in list_coins]
    except Exception:
        return 
    
def get_companies_holding_crypto(symbol):
    url = f"https://api.coingecko.com/api/v3/companies/public_treasury/{symbol}"
    try:
        list_coins = requests.get(url).json()["companies"]
        locale.setlocale(locale.LC_ALL, '')
        return [Company(record).__dict__ for record in list_coins]
    except Exception:
        return 