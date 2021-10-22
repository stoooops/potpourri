import json
from decimal import Decimal
from typing import Any, Dict

import requests


class CoinbaseClient:
    def __init__(self):
        self._base_url = "https://api.coinbase.com/v2/"

    def query(self, url) -> Dict[str, Any]:
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError(f"[{url}] Status Code: {response.status_code}")
        else:
            response_json = json.loads(response.content)

        return response_json

    def get_price(self, ticker: str) -> Decimal:
        route: str = f"prices/{ticker}-USD/buy"
        url = f"{self._base_url}{route}"

        response: Dict[str, Any] = self.query(url)
        return Decimal(response["data"]["amount"])
