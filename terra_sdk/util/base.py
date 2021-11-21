"""Some useful base classes to inherit from."""
from abc import abstractmethod
from typing import Any, Callable, Dict, List, Type

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
        ...

    @staticmethod
    @abstractmethod
    def from_proto(data: Message) -> "BaseTerraData":
        ...

    @abstractmethod
    def to_proto(self) -> Message:
        ...


def create_demux(inputs: List[Type[BaseTerraData]]) -> Callable[[Dict[str, Any]], Any]:
    table = {i.type_url: i.from_data for i in inputs}

    def from_data(data: dict) -> BaseTerraData:
        return table[data["@type"]](data)

    return from_data


def create_demux_proto(inputs: List[type[BaseTerraData]]) -> Callable[[Message], Any]:
    table = {i.type_url: i.from_proto for i in inputs}

    def from_proto(data: Message) -> BaseTerraData:
        return table[data["@type"]](data)

    return from_proto
