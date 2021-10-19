import json
from decimal import Decimal
from typing import Dict

import requests


class EtherscanClient:
    def __init__(self, api_key: str):
        self._base_url = f"https://api.etherscan.io/api?apikey={api_key}"

    def query(self, url) -> Dict[str, str]:
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError("Status Code: {r.status_code}")
        else:
            response_json = json.loads(response.content)

        return response_json

    def get_account_balance(self, account: str) -> Decimal:
        query_args = "&".join(["module=account", "action=balance", f"address={account}", "tag=latest"])
        url = f"{self._base_url}&{query_args}"

        response: Dict[str, str] = self.query(url)
        balance: str = response["result"]
        return Decimal(balance)
