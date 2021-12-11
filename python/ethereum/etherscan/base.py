from datetime import datetime, timezone
from typing import Dict, Optional


class TransactionHash(str):
    def __new__(cls, content):
        return str.__new__(cls, content)


class BaseEvent:
    def __init__(self, data: Dict[str, str]):
        self._data = data

        try:
            self._block_number: int = int(data["blockNumber"])
            self._contract_address: Optional[str] = (
                data["contractAddress"] if data["contractAddress"] is not None else None
            )
            self._from_address: str = data["from"]
            self._gas: int = int(data["gas"])  # gas
            self._gas_used = int(data["gasUsed"])
            self._hash: TransactionHash = TransactionHash(data["hash"])
            self._input: str = data["input"]
            self._timestamp: int = int(data["timeStamp"])
            self._to_address: str = data["to"]

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
    def timestamp_datetime(self) -> datetime:
        return datetime.fromtimestamp(self._timestamp).astimezone(tz=timezone.utc)

    @property
    def hash(self) -> TransactionHash:
        return self._hash

    @property
    def gas(self) -> int:
        return self._gas

    @property
    def gas_used(self) -> int:
        return self._gas_used

    @property
    def from_address(self) -> str:
        return self._from_address

    @property
    def to_address(self) -> str:
        return self._to_address

    @property
    def input(self) -> str:
        return self._input

    @property
    def contract_address(self) -> Optional[str]:
        return self._contract_address

    @property
    def json(self) -> Dict[str, str]:
        return self._data


class BaseEventDetailed(BaseEvent):
    def __init__(self, data: Dict[str, str]):
        super().__init__(data=data)

        try:
            self._block_hash: str = data["blockHash"]
            self._confirmations = int(data["confirmations"])
            self._cumulative_gas_used = int(data["cumulativeGasUsed"])
            self._gas_price: int = int(data["gasPrice"])  # wei
            self._nonce: int = int(data["nonce"])
            self._transaction_index: int = int(data["transactionIndex"])

        except Exception:
            print(f"Could not parse: {data}")
            raise

    @property
    def block_hash(self) -> str:
        return self._block_hash

    @property
    def confirmations(self) -> int:
        return self._confirmations

    @property
    def cumulative_gas_used(self) -> int:
        return self._cumulative_gas_used

    @property
    def gas_price(self) -> int:
        return self._gas_price

    @property
    def nonce(self) -> int:
        return self._nonce

    @property
    def transaction_index(self) -> int:
        return self._transaction_index
