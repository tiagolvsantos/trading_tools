import requests
import json


def get_crypto_fear_greed_index():
    url = "https://api.alternative.me/fng/?limit=10"
    try:
        return requests.get(url).json()
    except Exception:
        return {}
    