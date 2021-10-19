from decimal import Decimal
from typing import Dict, Optional

from potpourri.python.ethereum.etherscan.base import BaseEvent


class Transaction(BaseEvent):
    def __init__(self, data: Dict[str, str]):
        super().__init__(data=data)

        try:
            self._is_error: int = int(data["isError"])
            self._txreceipt_status: Optional[int] = (
                int(data["txreceipt_status"]) if data["txreceipt_status"] != "" else None
            )
            self._value: int = int(data["value"])  # wei
        except Exception:
            print(f"Could not parse: {data}")
            raise

    @property
    def is_error(self) -> int:
        return self._is_error

    @property
    def txreceipt_status(self) -> Optional[int]:
        return self._txreceipt_status

    @property
    def value_wei(self) -> int:
        return self._value

    @property
    def value_gwei(self) -> Decimal:
        return self._value / 10 ** 9

    @property
    def value_eth(self) -> Decimal:
        return self._value / 10 ** 18
