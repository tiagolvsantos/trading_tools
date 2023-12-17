from src.libs import utils
import requests
import json


class Flow:
  def __init__(self, query_json:json):
    self.Date = query_json["asOf"]
    self.Value = query_json["value"]


def get_etf_flow_data(symbol):
    url = f"https://api-prod.etf.com/private/apps/fundflows/{symbol}/charts?startDate={utils.get_last_n_days_date('%Y%m%d',90)}"
    try:
        json_data = requests.get(url).json()["data"]
        return [Flow(record).__dict__ for record in json_data["results"]["data"]]
    except Exception:
        return 
    
