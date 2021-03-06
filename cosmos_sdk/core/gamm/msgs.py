"""GAMM module message types."""
from __future__ import annotations

import attr
from cosmos_proto.osmosis.gamm.v1beta1 import MsgSwapExactAmountIn as MsgSwapExactAmountIn_pb
from cosmos_proto.osmosis.gamm.v1beta1 import MsgSwapExactAmountOut as MsgSwapExactAmountOut_pb

from cosmos_sdk.core import AccAddress, Coin
from cosmos_sdk.core.msg import Msg

from .data import SwapAmountInRoute, SwapAmountOutRoute

__all__ = ["MsgSwapExactAmountIn", "MsgSwapExactAmountOut"]


@attr.s
class MsgSwapExactAmountIn(Msg):
    type_amino = "osmosis/gamm/swap-exact-amount-in"
    """"""
    type_url = "/osmosis.gamm.v1beta1.MsgSwapExactAmountIn"
    """"""
    proto_msg = MsgSwapExactAmountIn_pb
    """"""

    sender: AccAddress = attr.ib()
    routes: list[SwapAmountInRoute] = attr.ib()
    tokenIn: Coin = attr.ib()
    tokenOutMinAmount: int = attr.ib(default=0)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "routes": [r.to_data() for r in self.routes],
                "tokenIn": self.tokenIn.to_data(),
                "tokenOutMinAmount": str(self.tokenOutMinAmount),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgSwapExactAmountIn:
        return cls(
            sender=data["sender"],
            routes=[SwapAmountInRoute.from_data(r) for r in data["routes"]],
            tokenIn=Coin.from_data(data["tokenIn"]),
            tokenOutMinAmount=int(data["tokenOutMinAmount"]),
        )

    @classmethod
    def from_proto(cls, proto: MsgSwapExactAmountIn_pb) -> MsgSwapExactAmountIn:
        return cls(
            sender=AccAddress(proto.sender),
            routes=[SwapAmountInRoute.from_proto(r) for r in proto.routes],
            tokenIn=Coin.from_proto(proto.token_in),
            tokenOutMinAmount=int(proto.token_out_min_amount),
        )

    def to_proto(self) -> MsgSwapExactAmountIn_pb:
        return MsgSwapExactAmountIn_pb(
            sender=self.sender,
            routes=[r.to_proto() for r in self.routes],
            token_in=self.tokenIn.to_proto(),
            token_out_min_amount=str(self.tokenOutMinAmount),
        )


@attr.s
class MsgSwapExactAmountOut(Msg):
    type_amino = "osmosis/gamm/swap-exact-amount-out"
    """"""
    type_url = "/osmosis.gamm.v1beta1.MsgSwapExactAmountOut"
    """"""
    proto_msg = MsgSwapExactAmountOut_pb
    """"""

    sender: AccAddress = attr.ib()
    routes: list[SwapAmountOutRoute] = attr.ib()
    tokenOut: Coin = attr.ib()
    tokenInMaxAmount: int = attr.ib(default=0)

    def to_amino(self) -> dict:
        return {
            "type": self.type_amino,
            "value": {
                "sender": self.sender,
                "routes": [r.to_data() for r in self.routes],
                "tokenOut": self.tokenOut.to_data(),
                "tokenInMaxAmount": str(self.tokenInMaxAmount),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgSwapExactAmountOut:
        return cls(
            sender=data["sender"],
            routes=[SwapAmountOutRoute.from_data(r) for r in data["routes"]],
            tokenOut=Coin.from_data(data["tokenOut"]),
            tokenInMaxAmount=int(data["tokenInMaxAmount"]),
        )

    @classmethod
    def from_proto(cls, proto: MsgSwapExactAmountOut_pb) -> MsgSwapExactAmountOut:
        return cls(
            sender=AccAddress(proto.sender),
            routes=[SwapAmountOutRoute.from_proto(r) for r in proto.routes],
            tokenOut=Coin.from_proto(proto.token_out),
            tokenInMaxAmount=int(proto.token_in_max_amount),
        )

    def to_proto(self) -> MsgSwapExactAmountOut_pb:
        return MsgSwapExactAmountOut_pb(
            sender=self.sender,
            routes=[r.to_proto() for r in self.routes],
            token_out=self.tokenOut.to_proto(),
            token_in_max_amount=str(self.tokenInMaxAmount),
        )
