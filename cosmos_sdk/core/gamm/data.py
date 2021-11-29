"""GAMM module data objects."""
from __future__ import annotations

import attr
from cosmos_proto.osmosis.gamm.v1beta1 import SwapAmountInRoute as SwapAmountInRoute_pb
from cosmos_proto.osmosis.gamm.v1beta1 import SwapAmountOutRoute as SwapAmountOutRoute_pb

__all__ = ["SwapAmountInRoute", "SwapAmountOutRoute"]


@attr.s
class SwapAmountInRoute:
    pool_id: int = attr.ib()
    token_out_denom: str = attr.ib()

    def to_data(self) -> dict:
        return {
            "tokenOutDenom": self.token_out_denom,
            "poolId": str(self.pool_id),
        }

    @classmethod
    def from_data(cls, data: dict) -> SwapAmountInRoute:
        return cls(
            token_out_denom=data["tokenOutDenom"],
            pool_id=int(data["poolId"]),
        )

    def to_proto(self) -> SwapAmountInRoute_pb:
        return SwapAmountInRoute_pb(pool_id=self.pool_id, token_out_denom=self.token_out_denom)

    @classmethod
    def from_proto(cls, proto: SwapAmountInRoute_pb) -> SwapAmountInRoute:
        return cls(
            token_out_denom=proto.token_out_denom,
            pool_id=proto.pool_id,
        )


@attr.s
class SwapAmountOutRoute:
    pool_id: int = attr.ib()
    token_in_denom: str = attr.ib()

    def to_data(self) -> dict:
        return {
            "tokenInDenom": self.token_in_denom,
            "poolId": str(self.pool_id),
        }

    @classmethod
    def from_data(cls, data: dict) -> SwapAmountOutRoute:
        return cls(
            token_in_denom=data["tokenInDenom"],
            pool_id=int(data["poolId"]),
        )

    def to_proto(self) -> SwapAmountOutRoute_pb:
        return SwapAmountOutRoute_pb(pool_id=self.pool_id, token_in_denom=self.token_in_denom)

    @classmethod
    def from_proto(cls, proto: SwapAmountOutRoute_pb) -> SwapAmountOutRoute:
        return cls(
            token_in_denom=proto.token_in_denom,
            pool_id=proto.pool_id,
        )
