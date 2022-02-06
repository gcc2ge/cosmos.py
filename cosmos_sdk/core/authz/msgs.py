"""Authz module message types."""

from __future__ import annotations

from typing import List

import attr
from betterproto.lib.google.protobuf import Any as Any_pb
from cosmos_proto.cosmos.authz.v1beta1 import MsgExec as MsgExec_pb
from cosmos_proto.cosmos.authz.v1beta1 import MsgGrant as MsgGrant_pb
from cosmos_proto.cosmos.authz.v1beta1 import MsgRevoke as MsgRevoke_pb

from cosmos_sdk.core import AccAddress
from cosmos_sdk.core.msg import Msg

from .data import Authorization, AuthorizationGrant

__all__ = ["MsgExecAuthorized", "MsgGrantAuthorization", "MsgRevokeAuthorization"]


@attr.s
class MsgExecAuthorized(Msg):
    """Execute a set of messages, exercising an existing authorization.

    Args:
        grantee: grantee account (submitting on behalf of granter)
        msg (List[Msg]): list of messages to execute using authorization grant
    """

    type_amino = "msgauth/MsgExecAuthorized"
    """"""
    type_url = "/cosmos.authz.v1beta1.MsgExec"
    """"""
    proto_msg = MsgExec_pb
    """"""

    grantee: AccAddress = attr.ib()
    msgs: List[Msg] = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "grantee": self.grantee,
                "msgs": [msg.to_amino() for msg in self.msgs],
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgExecAuthorized:
        return cls(grantee=data["grantee"], msgs=[Msg.from_data(md) for md in data["msgs"]])

    @classmethod
    def from_proto(cls, proto: MsgExec_pb) -> MsgExecAuthorized:
        return cls(
            grantee=AccAddress(proto.grantee),
            msgs=[Msg.from_proto(m) for m in proto.msgs],
        )

    def to_proto(self) -> MsgExec_pb:
        return MsgExec_pb(grantee=self.grantee, msgs=[m.pack_any() for m in self.msgs])


@attr.s
class MsgGrantAuthorization(Msg):
    """Grant an authorization to ``grantee`` to call messages on behalf of ``granter``.

    Args:
        granter: account granting authorization
        grantee: account receiving authorization
        grant: pair of authorization, expiration
    """

    type_amino = "msgauth/MsgGrantAuthorization"
    """"""
    type_url = "/cosmos.authz.v1beta1.MsgGrant"
    """"""
    proto_msg = MsgGrant_pb
    """"""

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    grant: AuthorizationGrant = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "granter": self.granter,
                "grantee": self.grantee,
                "grant": self.grant.to_amino(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgGrantAuthorization:
        data = data["value"]
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            grant=AuthorizationGrant(
                authorization=Authorization.from_data(data["grant"]["authorization"]),
                expiration=str(data["grant"]["expiration"]),
            ),
        )

    @classmethod
    def from_proto(cls, proto: MsgGrant_pb) -> MsgGrantAuthorization:
        return cls(
            granter=AccAddress(proto.granter),
            grantee=AccAddress(proto.grantee),
            grant=AuthorizationGrant.from_proto(proto.grant),
        )

    def to_proto(self) -> MsgGrant_pb:
        return MsgGrant_pb(
            granter=self.granter, grantee=self.grantee, grant=self.grant.to_proto()
        )


@attr.s
class MsgRevokeAuthorization(Msg):
    """Remove existing authorization grant of the specified message type.

    Args:
        granter: account removing authorization
        grantee: account having authorization removed
        msg_type_url: type of message to remove authorization for
    """

    type_amino = "msgauth/MsgRevokeAuthorization"
    """"""
    type_url = "/cosmos.authz.v1beta1.MsgRevoke"
    """"""

    granter: AccAddress = attr.ib()
    grantee: AccAddress = attr.ib()
    msg_type_url: str = attr.ib()

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "granter": self.granter,
                "grantee": self.grantee,
                "msg_type_url": self.msg_type_url,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgRevokeAuthorization:
        return cls(
            granter=data["granter"],
            grantee=data["grantee"],
            msg_type_url=data["msg_type_url"],
        )

    def to_proto(self) -> MsgRevoke_pb:
        return MsgRevoke_pb(
            granter=self.granter, grantee=self.grantee, msg_type_url=self.msg_type_url
        )
