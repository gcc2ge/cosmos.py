from __future__ import annotations

import base64
from abc import ABC, abstractmethod
from typing import TypeVar

import attr
from betterproto import Message
from betterproto.lib.google.protobuf import Any as Any_pb
from cosmos_proto.cosmos.crypto.ed25519 import PubKey as ValConsPubKey_pb
from cosmos_proto.cosmos.crypto.multisig import LegacyAminoPubKey as LegacyAminoPubKey_pb
from cosmos_proto.cosmos.crypto.secp256k1 import PubKey as SimplePubKey_pb

from cosmos_sdk.util.base import BaseTerraData

__all__ = ["PublicKey", "SimplePublicKey", "ValConsPubKey", "LegacyAminoPubKey"]

_PublicKeyT = TypeVar("_PublicKeyT", bound="PublicKey")


class PublicKey(BaseTerraData, ABC):
    """Data object holding the public key component of an account or signature."""

    @abstractmethod
    def get_type(self) -> str:
        return self.type_url

    @classmethod
    def from_proto(cls, proto: Message):
        from cosmos_sdk.util.parse_public_key import parse_pub_key_proto

        return parse_pub_key_proto(proto)

    @classmethod
    def from_data(cls, data: dict):
        from cosmos_sdk.util.parse_public_key import parse_pub_key

        return parse_pub_key(data)

    @abstractmethod
    def pack_any(self) -> Any_pb:
        ...

    @abstractmethod
    def to_amino(self: _PublicKeyT) -> _PublicKeyT:
        ...


@attr.s
class SimplePublicKey(PublicKey):
    """Data object holding the SIMPLE public key component of an account or signature."""

    type_amino = "tendermint/PubKeySecp256k1"
    """"""
    type_url = "/cosmos.crypto.secp256k1.PubKey"
    """"""
    proto_msg = SimplePubKey_pb
    """Normal signature public key type."""

    key: bytes = attr.ib()

    def to_amino(self) -> dict:
        return {"type": self.type_amino, "value": self.key}

    @classmethod
    def from_data(cls, data: dict) -> SimplePublicKey:
        return cls(key=data["key"])

    @classmethod
    def from_proto(cls, proto: SimplePubKey_pb) -> SimplePublicKey:
        return cls(proto.key)

    def to_proto(self) -> SimplePubKey_pb:
        return SimplePubKey_pb(key=self.key)

    def get_type(self) -> str:
        return self.type_url

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))


@attr.s
class ValConsPubKey(PublicKey):
    """Data object holding the public key component of an validator's account or signature."""

    type_amino = "tendermint/PubKeyEd25519"
    """"""
    type_url = "/cosmos.crypto.ed25519.PubKey"
    """"""
    proto_msg = ValConsPubKey_pb
    """an ed25519 tendermint public key type."""

    key: bytes = attr.ib()

    def to_amino(self) -> dict:
        return {"type": self.type_amino, "value": self.key}

    @classmethod
    def from_data(cls, data: dict) -> ValConsPubKey:
        return cls(key=data["key"])

    def get_type(self) -> str:
        return self.type_url

    @classmethod
    def from_proto(cls, proto: ValConsPubKey_pb) -> ValConsPubKey:
        return cls(proto.key)

    def to_proto(self) -> ValConsPubKey_pb:
        return ValConsPubKey_pb(key=base64.b64encode(self.key))

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))


# FIXME: NOT TESTED
@attr.s
class LegacyAminoPubKey(PublicKey):
    """Data object holding the Legacy Amino-typed public key component of an account or signature."""

    type_amino = "tendermint/PubKeyMultisigThreshold"
    """"""
    type_url = "/cosmos.crypto.multisig.LegacyAminoPubKey"
    """"""
    proto_msg = LegacyAminoPubKey_pb
    """Multisig public key type."""

    threshold: int = attr.ib(converter=int)
    public_keys: list[bytes] = attr.ib(factory=list)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "threshold": str(self.threshold),
                "pubkeys": [pubkey for pubkey in self.public_keys],
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> LegacyAminoPubKey:
        return cls(threshold=data["threshold"], public_keys=data["public_keys"])

    def get_type(self) -> str:
        return self.type_url

    @classmethod
    def from_proto(cls, proto: LegacyAminoPubKey_pb) -> LegacyAminoPubKey:
        return cls(proto.threshold, [k.value for k in proto.public_keys])

    def to_proto(self) -> LegacyAminoPubKey_pb:
        return LegacyAminoPubKey_pb(
            threshold=self.threshold,
            public_keys=[Any_pb(self.type_url, k) for k in self.public_keys],
        )

    def pack_any(self) -> Any_pb:
        return Any_pb(type_url=self.type_url, value=bytes(self.to_proto()))
