import json
from decimal import Decimal
from typing import Any, Dict, List, Optional

import requests
from potpourri.python.ethereum.etherscan.erc20 import ERC20Transfer
from potpourri.python.ethereum.etherscan.erc721 import ERC721Transfer
from potpourri.python.ethereum.etherscan.transaction import InternalTransaction, Transaction


class EtherscanClient:
    def __init__(self, api_key: str):
        self._base_url = f"https://api.etherscan.io/api?apikey={api_key}"

    @staticmethod
    def tx_url(hash_: str) -> str:
        return f"https://etherscan.io/tx/{hash_}"

    def query(self, url) -> Dict[str, Any]:
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

    def get_txlist(
        self,
        address: str,
        start_block: int = 0,
        end_block: int = 99999999,
        page: int = 1,
        offset: int = 0,
    ) -> List[Transaction]:
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

        response: Dict[str, Any] = self.query(url)
        result: List[Transaction] = [Transaction(t) for t in response["result"]]
        return result

    def get_txlistinternal(
        self,
        address: str,
        start_block: int = 0,
        end_block: int = 99999999,
        page: int = 1,
        offset: int = 0,
    ) -> List[InternalTransaction]:
        query_args = "&".join(
            [
                "module=account",
                "action=txlistinternal",
                f"address={address}",
                f"startblock={start_block}",
                f"endblock={end_block}",
                f"page={page}",
                f"offset={offset}",
                "sort=asc",
            ]
        )
        url = f"{self._base_url}&{query_args}"

        response: Dict[str, Any] = self.query(url)
        result: List[InternalTransaction] = [InternalTransaction(t) for t in response["result"]]
        return result

    def get_tokentx(
        self,
        address: str,
        contract_address: Optional[str] = "",
        start_block: int = 0,
        end_block: int = 99999999,
        page: int = 1,
        offset: int = 0,
    ) -> List[ERC20Transfer]:
        query_args_list = [
            "module=account",
            "action=tokentx",
            f"contract_address={contract_address}",
            f"address={address}",
            f"startblock={start_block}",
            f"endblock={end_block}",
            f"page={page}",
            f"offset={offset}",
            "sort=asc",
        ]

        query_args = "&".join(query_args_list)
        url = f"{self._base_url}&{query_args}"

        response: Dict[str, Any] = self.query(url)
        result: List[ERC20Transfer] = [ERC20Transfer(t) for t in response["result"]]
        return result

    def get_tokennfttx(
        self,
        address: str,
        contract_address: Optional[str] = "",
        start_block: int = 0,
        end_block: int = 99999999,
        page: int = 1,
        offset: int = 0,
    ) -> List[ERC721Transfer]:
        query_args_list = [
            "module=account",
            "action=tokennfttx",
            f"contract_address={contract_address}",
            f"address={address}",
            f"startblock={start_block}",
            f"endblock={end_block}",
            f"page={page}",
            f"offset={offset}",
            "sort=asc",
        ]

        query_args = "&".join(query_args_list)
        url = f"{self._base_url}&{query_args}"

        response: Dict[str, Any] = self.query(url)
        result: List[ERC721Transfer] = [ERC721Transfer(t) for t in response["result"]]
        return result
