"""Some useful base classes to inherit from."""
from typing import Any, Callable, Dict, List, Type, TypeVar

from betterproto import Message
from betterproto.lib.google.protobuf import Any as Any_pb

from .json import JSONSerializable, dict_to_data

_BaseTerraDataT = TypeVar("_BaseTerraDataT", bound="BaseTerraData")


class BaseTerraData(JSONSerializable, Message):

    type: str
    type_url: str

    def to_data(self) -> dict:
        return {"@type": self.type_url, **dict_to_data(self.__dict__)}

    @classmethod
    def from_data(cls: Type[_BaseTerraDataT], data: dict) -> _BaseTerraDataT:
        raise NotImplementedError

    @classmethod
    def from_proto(cls: Type[_BaseTerraDataT], data: Message) -> _BaseTerraDataT:
        raise NotImplementedError

    @classmethod
    def from_proto_bytes(cls: Type[_BaseTerraDataT], data: bytes) -> _BaseTerraDataT:
        raise NotImplementedError

    def to_proto(self) -> Message:
        raise NotImplementedError


def create_demux(inputs: List[Type[BaseTerraData]]) -> Callable[[Dict[str, Any]], Any]:
    table = {i.type_url: i.from_data for i in inputs}

    def from_data(data: dict) -> BaseTerraData:
        return table[data["@type"]](data)

    return from_data


def create_demux_proto(inputs: List[type[BaseTerraData]]) -> Callable[[Message], Any]:
    table = {i.type_url: i.from_proto for i in inputs}
    table_bytes = {i.type_url: i.from_proto_bytes for i in inputs}

    def from_proto(data: Message) -> BaseTerraData:
        if isinstance(data, Any_pb):
            return table_bytes[data.type_url](data.value)
        return table[data.type_url](data)

    return from_proto
