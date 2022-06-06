"""GAMM module data objects."""
from __future__ import annotations

import attr
from bech32 import List
from cosmos_proto.osmosis.gamm.v1beta1 import SwapAmountInRoute as SwapAmountInRoute_pb
from cosmos_proto.osmosis.gamm.v1beta1 import SwapAmountOutRoute as SwapAmountOutRoute_pb
from cosmos_sdk.core import Dec
from cosmos_sdk.core import Coin

__all__ = ["SwapAmountInRoute", "SwapAmountOutRoute"]


@attr.s
class PoolParams:
    swap_fee: Dec = attr.ib(converter=Dec)
    exit_fee: Dec = attr.ib(converter=Dec)

    def to_data(self) -> dict:
        return {
            "swapFee": str(self.swap_fee),
            "exitFee": str(self.exit_fee),
        }

    @classmethod
    def from_data(cls, data: dict) -> PoolParams:
        return cls(
            swap_fee=data["swapFee"],
            exit_fee=data["exitFee"],
        )

@attr.s
class PoolAsset:
    token: Coin = attr.ib(converter=Coin.parse)
    weight: Dec = attr.ib(converter=Dec)

    def to_data(self) -> dict:
        return {
            "token": self.token.to_data(),
            "weight": str(self.weight),
        }

    @classmethod
    def from_data(cls, data: dict) -> PoolParams:
        return cls(
            token = Coin.from_data(data["token"]),
            weight = data["weight"],
        )
@attr.s
class PoolAssets:
    ...

@attr.s
class Pool:
    id: int = attr.ib()
    pool_params: PoolParams=attr.ib()
    total_shares: Coin = attr.ib(converter=Coin.parse)
    pool_assets: List[PoolAsset] = attr.ib()
    total_weight: Dec = attr.ib(converter=Dec)


    def to_data(self) -> dict:
        return {
            "id": str(self.id),
            "poolParams": self.pool_params.to_data(),
            "totalShares": self.total_shares.to_data(),
            "poolAssets": [ pool_asset.to_data() for pool_asset in self.pool_assets],
            "totalWeight": self.total_weight.to_data()
        }

    @classmethod
    def from_data(cls, data: dict) -> SwapAmountInRoute:
        return cls(
            id = int(data["id"]),
            pool_params = PoolParams.from_data(data['poolParams']),
            total_shares = Coin.from_data(data["totalShares"]),
            pool_assets = [ PoolAsset.from_data(asset) for asset in data["poolAssets"]],
            total_weight = data["totalWeight"]
        )

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
