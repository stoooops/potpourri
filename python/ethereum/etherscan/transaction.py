from decimal import Decimal
from typing import Dict, Optional


class Transaction:
    def __init__(self, data: Dict[str, str]):
        self._data = data

        try:
            self._block_number: int = int(data["blockNumber"])
            self._timestamp: int = int(data["timeStamp"])
            self._hash: str = data["hash"]
            self._nonce: int = int(data["nonce"])
            self._block_hash: str = data["blockHash"]
            self._transaction_index: int = int(data["transactionIndex"])
            self._from_address: str = data["from"]
            self._to_address: str = data["to"]
            self._value: int = int(data["value"])  # wei
            self._gas: int = int(data["gas"])  # gas
            self._gas_price: int = int(data["gasPrice"])  # wei
            self._is_error: int = int(data["isError"])
            self._txreceipt_status: Optional[int] = (
                int(data["txreceipt_status"]) if data["txreceipt_status"] != "" else None
            )
            self._input: str = data["input"]
            self._contract_address: Optional[str] = (
                data["contractAddress"] if data["contractAddress"] is not None else None
            )
            self._cumulative_gas_used = int(data["cumulativeGasUsed"])
            self._gas_used = int(data["gasUsed"])
            self._confirmations = int(data["confirmations"])
        except Exception:
            print(f"Could not parse: {data}")
            raise

    @property
    def block_number(self) -> int:
        return self._block_number

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def nonce(self) -> int:
        return self._nonce

    @property
    def block_hash(self) -> str:
        return self._block_hash

    @property
    def transaction_index(self) -> int:
        return self._transaction_index

    @property
    def from_address(self) -> str:
        return self._from_address

    @property
    def to_address(self) -> str:
        return self._to_address

    @property
    def value_wei(self) -> int:
        return self._value

    @property
    def value_gwei(self) -> Decimal:
        return self._value / 10 ** 9

    @property
    def value_eth(self) -> Decimal:
        return self._value / 10 ** 18

    @property
    def gas(self) -> int:
        return self._gas

    @property
    def gas_price(self) -> int:
        return self._gas_price

    @property
    def is_error(self) -> int:
        return self._is_error

    @property
    def txreceipt_status(self) -> Optional[int]:
        return self._txreceipt_status

    @property
    def input(self) -> str:
        return self._input

    @property
    def contract_address(self) -> Optional[str]:
        return self._contract_address

    @property
    def cumulative_gas_used(self) -> int:
        return self._cumulative_gas_used

    @property
    def gas_used(self) -> int:
        return self._gas_used

    @property
    def confirmations(self) -> int:
        return self._confirmations

    @property
    def json(self) -> Dict[str, str]:
        return self._data
