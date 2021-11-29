"""Gov module governance proposal types."""

from __future__ import annotations

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from cosmos_proto.cosmos.gov.v1beta1 import TextProposal as TextProposal_pb

from cosmos_sdk.util.base import BaseTerraData

__all__ = ["TextProposal"]


@attr.s
class TextProposal(BaseTerraData):
    """Generic proposal type with only title and description that does nothing if
    passed. Primarily used for assessing the community sentiment around the proposal.

    Args:
        title: proposal title
        description: proposal description
    """
    type_amino = "gov/TextProposal"
    """"""
    type_url = "/cosmos.gov.v1beta1.TextProposal"
    """"""
    proto_msg = TextProposal_pb
    """"""

    title: str = attr.ib()
    description: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description
            }
        }

    @classmethod
    def from_data(cls, data: dict) -> TextProposal:
        return cls(title=data["title"], description=data["description"])

    @classmethod
    def from_proto(cls, proto: TextProposal_pb) -> TextProposal:
        return cls(title=proto.title, description=proto.description)

    def to_proto(self) -> TextProposal_pb:
        return TextProposal_pb(title=self.title, description=self.description)

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))
