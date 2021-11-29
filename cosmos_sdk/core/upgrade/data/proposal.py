"""Upgrade module data objects."""

from __future__ import annotations

__all__ = ["SoftwareUpgradeProposal", "CancelSoftwareUpgradeProposal"]

from typing import Optional

import attr
from cosmos_proto.cosmos.upgrade.v1beta1 import (
    CancelSoftwareUpgradeProposal as CancelSoftwareUpgradeProposal_pb,
)
from cosmos_proto.cosmos.upgrade.v1beta1 import (
    SoftwareUpgradeProposal as SoftwareUpgradeProposal_pb,
)

from cosmos_sdk.core.upgrade.plan import Plan
from cosmos_sdk.util.base import BaseTerraData


@attr.s
class SoftwareUpgradeProposal(BaseTerraData):
    title: str = attr.ib()
    description: str = attr.ib()
    plan: Optional[Plan] = attr.ib()

    type_amino = "upgrade/SoftwareUpgradeProposal"
    """"""
    type_url = "/cosmos.upgrade.v1beta1.SoftwareUpgradeProposal"
    """"""
    proto_msg = SoftwareUpgradeProposal_pb
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
                "plan": self.plan.to_amino() if self.plan else None
            }
        }

    @classmethod
    def from_data(cls, data: dict) -> SoftwareUpgradeProposal:
        return cls(
            title=data["title"],
            description=data["description"],
            plan=Plan.from_data(data["plan"]) if data.get("plan") else None,
        )

    @classmethod
    def from_proto(cls, proto: SoftwareUpgradeProposal_pb) -> SoftwareUpgradeProposal:
        return cls(
            title=proto.title,
            description=proto.description,
            plan=Plan.from_proto(proto.plan),
        )

    def to_proto(self) -> SoftwareUpgradeProposal_pb:
        return SoftwareUpgradeProposal_pb(
            title=self.title,
            description=self.description,
            plan=self.plan.to_proto() if self.plan else None,
        )


@attr.s
class CancelSoftwareUpgradeProposal(BaseTerraData):
    title: str = attr.ib()
    description: str = attr.ib()

    type_amino = "upgrade/CancelSoftwareUpgradeProposal"
    """"""
    type_url = "/cosmos.upgrade.v1beta1.CancelSoftwareUpgradeProposal"
    """"""
    proto_msg = CancelSoftwareUpgradeProposal_pb
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "title": self.title,
                "description": self.description,
            }
        }

    @classmethod
    def from_data(cls, data: dict) -> CancelSoftwareUpgradeProposal:
        return cls(title=data["title"], description=data["description"])

    @classmethod
    def from_proto(cls, proto: CancelSoftwareUpgradeProposal_pb) -> CancelSoftwareUpgradeProposal:
        return cls(title=proto.title, description=proto.description)

    def to_proto(self) -> CancelSoftwareUpgradeProposal_pb:
        return CancelSoftwareUpgradeProposal_pb(
            title=self.title, description=self.description
        )
