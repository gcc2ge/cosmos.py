"""Data objects pertaining to accounts."""

from __future__ import annotations

from typing import List, Optional

import attr
from terra_proto.cosmos.auth.v1beta1 import BaseAccount as BaseAccount_pb

from ....core import AccAddress, Coins
from ....util.json import JSONSerializable
from ...public_key import PublicKey

__all__ = ["BaseAccount"]


@attr.s
class BaseAccount(JSONSerializable):
    """Stores information about an account."""

    type_amino = "core/Account"
    type_url = "/cosmos.auth.v1beta1.BaseAccount"
    proto_msg = BaseAccount_pb

    address: AccAddress = attr.ib()
    """"""

    public_key: Optional[PublicKey] = attr.ib()
    """"""

    account_number: int = attr.ib(converter=int)
    """"""

    sequence: int = attr.ib(converter=int)
    """"""

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "address": self.address,
                "public_key": self.public_key.to_amino() if self.public_key else None,
                "account_number": self.account_number,
                "sequence": self.sequence
            }
        }

    def get_sequence(self) -> int:
        return self.sequence

    def get_public_key(self) -> PublicKey | None:
        return self.public_key

    def to_data(self) -> dict:
        return {
            "@type": self.type_url,
            "address": self.address,
            "public_key": self.public_key and self.public_key.to_data(),
            "account_number": str(self.account_number),
            "sequence": str(self.sequence),
        }

    @classmethod
    def from_data(cls, data: dict) -> BaseAccount:
        return cls(
            address=data["address"],
            public_key=PublicKey.from_data(data["public_key"]) if "public_key" in data else None,
            account_number=data.get("account_number", 0),
            sequence=data.get("sequence", 0),
        )

    @classmethod
    def from_proto(cls, proto: BaseAccount_pb) -> BaseAccount:
        return cls(
            address=AccAddress(proto.address),
            public_key=PublicKey.from_proto(proto.pub_key),
            account_number=proto.account_number,
            sequence=proto.sequence,
        )

    @classmethod
    def from_proto_bytes(cls, data: bytes) -> BaseAccount:
        return cls.from_proto(BaseAccount_pb.FromString(data))

    def to_proto(self) -> BaseAccount_pb:
        return BaseAccount_pb(
            address=self.address,
            pub_key=self.public_key.to_proto() if self.public_key else None,
            account_number=self.account_number,
            sequence=self.sequence,
        )
