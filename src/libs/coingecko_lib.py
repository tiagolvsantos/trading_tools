import requests
import json


class Token:
  def __init__(self, query_json:json):
    self.Name = query_json["item"]["name"]
    self.symbol = query_json["item"]["symbol"]
    self.price = query_json["item"]["data"]["price"]
    self.percentage_change = f'{round(float(query_json["item"]["data"]["price_change_percentage_24h"]["usd"]),2)}%'
    self.total_volume = query_json["item"]["data"]["total_volume"]
    self.market_cap = query_json["item"]["data"]["market_cap"]


def get_trending_coins():
    url = "https://api.coingecko.com/api/v3/search/trending"
    try:
        list_coins = requests.get(url).json()["coins"]
        return [Token(record).__dict__ for record in list_coins]
    except Exception:
        return 