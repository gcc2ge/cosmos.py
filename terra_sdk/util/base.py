"""Some useful base classes to inherit from."""
from abc import abstractmethod
from typing import Any, Callable, Dict, List

from betterproto import Message

from .json import JSONSerializable, dict_to_data


class BaseTerraData(JSONSerializable, Message):

    type: str
    type_url: str

    def to_data(self) -> dict:
        return {"@type": self.type_url, **dict_to_data(self.__dict__)}

    @staticmethod
    @abstractmethod
    def from_data(data: dict) -> "BaseTerraData":
        pass

    @abstractmethod
    def to_proto(self):
        pass


def create_demux(inputs: List[BaseTerraData]) -> Callable[[Dict[str, Any]], Any]:
    table = {i.type_url: i.from_data for i in inputs}

    def from_data(data: dict):
        return table[data["@type"]](data)

    return from_data
