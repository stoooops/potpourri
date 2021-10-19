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

    def get_account_balance(self, address: str) -> Decimal:
        query_args = "&".join(["module=account", "action=balance", f"address={address}", "tag=latest"])
        url = f"{self._base_url}&{query_args}"

        response: Dict[str, str] = self.query(url)
        balance: str = response["result"]
        return Decimal(balance)

    def get_txlist(self, address: str, start_block: int = 0, end_block: int = 99999999, page: int = 1, offset: int = 0):
        query_args = "&".join(
            [
                "module=account",
                "action=txlist",
                f"address={address}",
                f"startblock={start_block}",
                f"endblock={end_block}",
                f"page={page}",
                f"offset={offset}",
                "sort=asc",
            ]
        )
        url = f"{self._base_url}&{query_args}"

        response: Dict[str, str] = self.query(url)
        result: str = response["result"]
        return result
