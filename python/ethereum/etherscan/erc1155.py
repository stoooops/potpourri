from typing import Dict

from potpourri.python.ethereum.etherscan.base import BaseEventDetailed


class ERC1155Transfer(BaseEventDetailed):
    def __init__(self, data: Dict[str, str]):
        super().__init__(data=data)

        assert self._input == "deprecated", f"Expected 'deprecated' value for 'input'. Got: '{self._input}'"

        self._token_id: int = int(data["tokenID"])
        self._token_name: str = data["tokenName"]
        self._token_symbol: str = data["tokenSymbol"]
        self._token_value: int = int(data["tokenValue"])

    @property
    def token_id(self) -> int:
        return self._token_id

    @property
    def token_name(self) -> str:
        return self._token_name

    @property
    def token_symbol(self) -> str:
        return self._token_symbol

    @property
    def token_value(self) -> int:
        return self._token_value
