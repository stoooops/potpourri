from decimal import Decimal
from typing import Dict, Optional

from potpourri.python.ethereum.etherscan.base import BaseEvent, BaseEventDetailed


class Transaction(BaseEventDetailed):
    def __init__(self, data: Dict[str, str]):
        super().__init__(data=data)

        try:
            self._is_error: int = int(data["isError"])
            self._txreceipt_status: Optional[int] = (
                int(data["txreceipt_status"]) if data["txreceipt_status"] != "" else None
            )
            self._value: int = int(data["value"])  # wei
        except Exception:
            # no logging this deep in the library?
            raise

    @property
    def is_error(self) -> int:
        return self._is_error

    @property
    def txreceipt_status(self) -> Optional[int]:
        return self._txreceipt_status

    @property
    def fee_wei(self) -> int:
        return self._gas_used * self._gas_price

    @property
    def fee_gwei(self) -> Decimal:
        return Decimal(self._gas_used * self._gas_price) / 10 ** 9

    @property
    def fee_eth(self) -> Decimal:
        return Decimal(self._gas_used * self._gas_price) / 10 ** 18

    @property
    def value_wei(self) -> int:
        return self._value

    @property
    def value_gwei(self) -> Decimal:
        return Decimal(self._value) / Decimal(10 ** 9)

    @property
    def value_eth(self) -> Decimal:
        return Decimal(self._value) / Decimal(10 ** 18)


class InternalTransaction(BaseEvent):
    def __init__(self, data: Dict[str, str]):
        super().__init__(data=data)

        try:
            self._is_error: int = int(data["isError"])
            self._value: int = int(data["value"])  # wei
        except Exception:
            # no logging this deep in the library?
            raise

    @property
    def is_error(self) -> int:
        return self._is_error

    @property
    def value_wei(self) -> int:
        return self._value

    @property
    def value_gwei(self) -> Decimal:
        return Decimal(self._value) / Decimal(10 ** 9)

    @property
    def value_eth(self) -> Decimal:
        return Decimal(self._value) / Decimal(10 ** 18)
