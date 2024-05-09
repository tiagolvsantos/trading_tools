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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url, headers=headers)
        data = response.json()["data"]
        return [Flow(record).__dict__ for record in data["results"]["data"]]
    except Exception:
        return 
    
