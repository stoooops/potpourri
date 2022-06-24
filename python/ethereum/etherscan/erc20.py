from decimal import Decimal
from typing import Dict

from potpourri.python.ethereum.etherscan.base import BaseEventDetailed


class ERC20Transfer(BaseEventDetailed):
    def __init__(self, data: Dict[str, str]):
        super().__init__(data=data)

        assert self._input == "deprecated", f"Expected 'deprecated' value for 'input'. Got: '{self._input}'"

        self._token_decimal: int = int(data["tokenDecimal"])
        self._token_name: str = data["tokenName"]
        self._token_symbol: str = data["tokenSymbol"]

        self._value: int = int(data["value"])

    @property
    def token_decimal(self) -> int:
        return self._token_decimal

    @property
    def token_name(self) -> str:
        return self._token_name

    @property
    def token_symbol(self) -> str:
        return self._token_symbol

    @property
    def value(self) -> int:
        return self._value

    @property
    def value_decimal(self) -> Decimal:
        return Decimal(self._value) / Decimal(10 ** self._token_decimal)
