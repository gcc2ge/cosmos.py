from __future__ import annotations

from betterproto import Message
from betterproto.lib.google.protobuf import Any as Any_pb

from cosmos_sdk.util.base import BaseTerraData


class Msg(BaseTerraData, Message):
    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))

    @staticmethod
    def from_data(data: dict) -> Msg:
        from cosmos_sdk.util.parse_msg import parse_msg

        return parse_msg(data)

    @staticmethod
    def from_proto(data: Message) -> Msg:
        from cosmos_sdk.util.parse_msg import parse_proto

        return parse_proto(data)
