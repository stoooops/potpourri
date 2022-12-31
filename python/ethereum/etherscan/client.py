import json
from decimal import Decimal
from typing import Any, Dict, List, Optional

import requests
from potpourri.python.ethereum.etherscan.erc20 import ERC20Transfer
from potpourri.python.ethereum.etherscan.erc721 import ERC721Transfer
from potpourri.python.ethereum.etherscan.erc1155 import ERC1155Transfer
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

    # https://api.etherscan.io/api
    #    ?module=account
    #    &action=tokentx
    #    &contractaddress=0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2
    #    &address=0x4e83362442b8d1bec281594cea3050c8eb01311c
    #    &page=1
    #    &offset=100
    #    &startblock=0
    #    &endblock=27025780
    #    &sort=asc
    #    &apikey=YourApiKeyToken
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

    # https://api.etherscan.io/api
    #    ?module=account
    #    &action=tokennfttx
    #    &contractaddress=0x06012c8cf97bead5deae237070f9587f8e7a266d
    #    &address=0x6975be450864c02b4613023c2152ee0743572325
    #    &page=1
    #    &offset=100
    #    &startblock=0
    #    &endblock=27025780
    #    &sort=asc
    #    &apikey=YourApiKeyToken
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

    # https://api.etherscan.io/api
    #    ?module=account
    #    &action=token1155tx
    #    &contractaddress=0x76be3b62873462d2142405439777e971754e8e77
    #    &address=0x83f564d180b58ad9a02a449105568189ee7de8cb
    #    &page=1
    #    &offset=100
    #    &startblock=0
    #    &endblock=99999999
    #    &sort=asc
    #    &apikey=YourApiKeyToken
    def get_token1155tx(
        self,
        address: str,
        contract_address: Optional[str] = "",
        start_block: int = 0,
        end_block: int = 99999999,
        page: int = 1,
        offset: int = 0,
    ) -> List[ERC1155Transfer]:
        query_args_list = [
            "module=account",
            "action=token1155tx",
            f"contract_address={contract_address}",
            f"address={address}",
            f"page={page}",
            f"offset={offset}",
            f"startblock={start_block}",
            f"endblock={end_block}",
            "sort=asc",
        ]

        query_args = "&".join(query_args_list)
        url = f"{self._base_url}&{query_args}"

        response: Dict[str, Any] = self.query(url)
        result: List[ERC1155Transfer] = [ERC1155Transfer(t) for t in response["result"]]
        return result
