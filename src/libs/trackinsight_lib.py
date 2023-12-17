import requests
import json

class Holding:
  def __init__(self, query_json:json):
    self.Name = query_json["label"]
    self.weight = f"{round(float(query_json['weight']),2)*100}%"

def get_etf_x_ray(symbol):
    url = f"https://data.trackinsight.com/holdings/{symbol}.json"
    json_result = requests.get(url).json()
    return [Holding(record).__dict__ for record in json_result["topHoldings"]]