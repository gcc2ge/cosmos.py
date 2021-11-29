"""Distribution module governance proposal types."""

from __future__ import annotations

import attr
from cosmos_proto.cosmos.distribution.v1beta1 import (
    CommunityPoolSpendProposal as CommunityPoolSpendProposal_pb,
)

from cosmos_sdk.core import AccAddress, Coins
from cosmos_sdk.util.base import BaseTerraData

__all__ = ["CommunityPoolSpendProposal"]


@attr.s
class CommunityPoolSpendProposal(BaseTerraData):
    """Proposal for allocating funds from the community pool to an address.

    Args:
        title: proposal title
        description: proposal description
        recipient: designated recipient of funds if proposal passes
        amount (Coins): amount to spend from community pool
    """

    type_amino = "distribution/CommunityPoolSpendProposal"
    """"""
    type_url = "/cosmos.distribution.v1beta1.CommunityPoolSpendProposal"
    """"""
    proto_msg = CommunityPoolSpendProposal_pb
    """"""

    title: str = attr.ib()
    description: str = attr.ib()
    recipient: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "recipient": self.recipient,
                "amount": self.amount.to_amino()
            }
        }

    @classmethod
    def from_data(cls, data: dict) -> CommunityPoolSpendProposal:
        return cls(
            title=data["title"],
            description=data["description"],
            recipient=data["recipient"],
            amount=Coins.from_data(data["amount"]),
        )

    @classmethod
    def from_proto(cls, proto: CommunityPoolSpendProposal_pb) -> CommunityPoolSpendProposal:
        return cls(
            title=proto.title,
            description=proto.description,
            recipient=AccAddress(proto.recipient),
            amount=Coins.from_proto(proto.amount),
        )

    def to_proto(self) -> CommunityPoolSpendProposal_pb:
        return CommunityPoolSpendProposal_pb(
            title=self.title,
            description=self.description,
            recipient=self.recipient,
            amount=self.amount.to_proto(),
        )
