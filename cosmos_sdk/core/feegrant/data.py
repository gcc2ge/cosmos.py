"""feegrant module data objects."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import TypeVar

import attr
from betterproto import Message
from dateutil import parser
from cosmos_proto.cosmos.feegrant.v1beta1 import (
    AllowedMsgAllowance as AllowedMsgAllowance_pb,
)
from cosmos_proto.cosmos.feegrant.v1beta1 import BasicAllowance as BasicAllowance_pb
from cosmos_proto.cosmos.feegrant.v1beta1 import (
    PeriodicAllowance as PeriodicAllowance_pb,
)

from cosmos_sdk.core import Coins
from cosmos_sdk.util.base import BaseTerraData
from cosmos_sdk.util.converter import to_isoformat

__all__ = ["BasicAllowance", "PeriodicAllowance", "AllowedMsgAllowance", "Allowance"]

_AllowanceT = TypeVar("_AllowanceT", bound="Allowance")


class Allowance(BaseTerraData, ABC):
    @classmethod
    def from_data(cls, data: dict) -> Allowance:
        from cosmos_sdk.util.parse_feegrant import parse_feegrant
        return parse_feegrant(data)

    @classmethod
    def from_proto(cls, data: Message) -> Allowance:
        from cosmos_sdk.util.parse_feegrant import parse_feegrant_proto
        return parse_feegrant_proto(data)

    @abstractmethod
    def to_proto(self: _AllowanceT) -> _AllowanceT:
        ...


@attr.s
class BasicAllowance(Allowance):
    """
    BasicAllowance implements Allowance with a one-time grant of tokens
    that optionally expires. The grantee can use up to SpendLimit to cover fees.
    """

    type_amino = "feegrant/BasicAllowance"
    """"""
    type_url = "/cosmos.feegrant.v1beta1.BasicAllowance"
    """"""
    proto_msg = BasicAllowance_pb
    """"""

    spend_limit: Coins = attr.ib(converter=Coins)
    expiration: datetime = attr.ib(converter=parser.parse)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "spend_limit": self.spend_limit.to_amino(),
                "expiration": to_isoformat(self.expiration)
            }
        }

    @classmethod
    def from_data(cls, data: dict) -> BasicAllowance:
        return cls(
            spend_limit=Coins.from_data(data["spend_limit"]),
            expiration=data["expiration"],
        )

    @classmethod
    def from_proto(cls, proto: BasicAllowance_pb) -> BasicAllowance:
        return cls(
            spend_limit=Coins.from_proto(proto.spend_limit),
            expiration=proto.expiration,
        )

    def to_proto(self) -> BasicAllowance_pb:
        return BasicAllowance_pb(
            spend_limit=self.spend_limit.to_proto(), expiration=self.expiration
        )


@attr.s
class PeriodicAllowance(Allowance):
    """
    PeriodicAllowance extends Allowance to allow for both a maximum cap,
     as well as a limit per time period.
    """

    type_amino = "feegrant/PeriodicAllowance"
    """"""
    type_url = "/cosmos.feegrant.v1beta1.PeriodicAllowance"
    """"""
    proto_msg = PeriodicAllowance_pb
    """"""

    basic: BasicAllowance = attr.ib()
    period: int = attr.ib(converter=int)
    period_spend_limit: Coins = attr.ib(converter=Coins)
    period_can_spend: Coins = attr.ib(converter=Coins)
    period_reset: datetime = attr.ib(converter=parser.parse)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "basic": self.basic.to_amino(),
                "period": str(self.period),
                "period_spend_limit": self.period_spend_limit.to_amino(),
                "period_can_spend": self.period_can_spend.to_amino(),
                "period_reset": to_isoformat(self.period_reset)
            }
        }

    @classmethod
    def from_data(cls, data: dict) -> PeriodicAllowance:
        return cls(
            basic=BasicAllowance.from_data(data["basic"]),
            period=data["period"],
            period_spend_limit=Coins.from_data(data["period_spend_limit"]),
            period_can_spend=Coins.from_data(data["period_can_spend"]),
            period_reset=data["period_reset"],
        )

    def to_proto(self) -> PeriodicAllowance_pb:
        return PeriodicAllowance_pb(
            basic=self.basic.to_proto(),
            period=timedelta(self.period),
            period_spend_limit=self.period_spend_limit.to_proto(),
            period_can_spend=self.period_can_spend.to_proto(),
            period_reset=self.period_reset,
        )


@attr.s
class AllowedMsgAllowance(Allowance):
    """
    AllowedMsgAllowance creates allowance only for specified message types.
    """

    type_amino = "feegrant/AllowedMsgAllowance"
    """"""
    type_url = "/cosmos.feegrant.v1beta1.AllowedMsgAllowance"
    """"""
    proto_msg = AllowedMsgAllowance_pb
    """"""

    allowance: Allowance = attr.ib()
    allowed_messages: list[str] = attr.ib(converter=list)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "allowance": self.allowance.to_amino(),
                "allowed_messages": self.allowed_messages
            }
        }

    @classmethod
    def from_data(cls, data: dict) -> AllowedMsgAllowance:
        allowance = data["allowance"]
        return cls(
            allowance=Allowance.from_data(allowance),
            allowed_messages=data["allowed_messages"],
        )

    def to_proto(self) -> AllowedMsgAllowance_pb:
        return AllowedMsgAllowance_pb(
            allowance=self.allowance.to_proto(),  # type: ignore
            allowed_messages=self.allowed_messages,
        )
