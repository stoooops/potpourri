from datetime import datetime
from decimal import Decimal
from typing import Any, Dict

from potpourri.python.ethereum.constants import BYZANTIUM, CONSTANTINOPLE


def get_base_reward(num: int) -> int:
    if num <= BYZANTIUM:
        return 5000000000000000000

    elif num <= CONSTANTINOPLE:
        return 3000000000000000000

    else:
        return 2000000000000000000


class BaseBlock:
    """
    An Ethereum block
    """
    def __init__(self, data: Dict[str, str]):
        self._data: Dict[str, Any] = data

        self._base_fee_per_gas_hex = data["baseFeePerGas"]
        self._base_fee_per_gas: int = int(self._base_fee_per_gas_hex, 16)

        self._difficulty_hex = data["difficulty"]
        self._difficulty: int = int(self._difficulty_hex, 16)

        self._gas_limit_hex = data["gasLimit"]
        self._gas_limit: int = int(self._gas_limit_hex, 16)

        self._gas_used_hex = data["gasUsed"]
        self._gas_used: int = int(self._gas_used_hex, 16)

        self._hash: str = data["hash"]
        self._logsBloom: str = data["logsBloom"]
        self._miner: str = data["miner"]
        self._mix_hash: str = data["mixHash"]
        self._nonce: str = data["nonce"]

        self._number_hex = data["number"]
        self._number: int = int(self._number_hex, 16)

        self._parentHash: str = data["parentHash"]
        self._receiptsRoot = data["receiptsRoot"]
        self._sha3_uncles = data["sha3Uncles"]
        self._size = data["size"]
        self._state_root = data["stateRoot"]

        self._timestamp_hex = data["timestamp"]
        self._timestamp: int = int(self._timestamp_hex, 16)

    @property
    def number(self) -> int:
        return self._number

    @property
    def base_issuance(self) -> int:
        return get_base_reward(self._number)

    @property
    def base_issuance_eth(self) -> int:
        return Decimal(self.base_issuance) / Decimal(10 ** 18)

    @property
    def json(self) -> Dict[str, Any]:
        return self._data

    @property
    def burned_eth(self) -> Decimal:
        burnt_wei = Decimal(self._gas_used) * Decimal(self._base_fee_per_gas)
        burnt_eth = burnt_wei / Decimal(10 ** 18)
        return burnt_eth

    @property
    def timestamp_dt(self) -> datetime:
        return datetime.fromtimestamp(self._timestamp)

    @property
    def day_dt(self) -> datetime:
        return self.timestamp_dt.replace(hour=0, minute=0, second=0, microsecond=0)

    @property
    def hour_dt(self) -> datetime:
        return self.timestamp_dt.replace(minute=0, second=0, microsecond=0)

    def __str__(self) -> str:
        return str(vars(self))


class Block(BaseBlock):
    """
    A mined Ethereum block.
    """
    def __init__(self, data: Dict[str, str]):
        super().__init__(data)
        self._total_difficulty = data["totalDifficulty"]


class UncleBlock(BaseBlock):
    """
    An Ethereum uncle block.
    """
    def __init__(self, data: Dict[str, Any], mined_block_num: int, uncle_index: int):
        super().__init__(data)

        self.mined_block_num: int = mined_block_num
        self.uncle_index: int = uncle_index

    @property
    def uncle_reward(self) -> Decimal:
        if (self._number + 8) < self.mined_block_num:
            return 0

        base_reward = get_base_reward(self.mined_block_num)
        diff = Decimal(self._number + 8 - self.mined_block_num)
        return Decimal(base_reward / 8) * diff
