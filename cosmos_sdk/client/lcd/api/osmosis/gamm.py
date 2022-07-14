from cosmos_sdk.core import Coin, Dec

from .._base import BaseAsyncAPI, sync_bind

from cosmos_sdk.core.gamm import Pool
from ...params import APIParams

from typing import List, Tuple, Dict, Optional

__all__ = ["AsyncGAMMAPI", "GAMMAPI"]


class AsyncGAMMAPI(BaseAsyncAPI):
    
    async def num_pools(self) -> Dec:
        res = await self._c._get("/osmosis/gamm/v1beta1/num_pools")
        return Dec(res.get("numPools"))

    async def pools(
        self,
        params: Optional[APIParams] = None,
    ) -> Tuple[List[Pool], Dict]:
        res = await self._c._get(f"/osmosis/gamm/v1beta1/pools", params)
        return [Pool.from_data(x) for x in res["pools"]], res.get("pagination")

    async def pool(
        self,
        pool_id: int,
    ) -> Pool:
        res = await self._c._get(f"/osmosis/gamm/v1beta1/pools/{pool_id}")
        return Pool.from_data(res["pool"])

    async def pool_liquidity(
        self,
        pool_id: int,
    ) -> List[Coin]:
        res = await self._c._get(f"/osmosis/gamm/v1beta1/pools/{pool_id}/total_pool_liquidity")
        
        # https://github.com/osmosis-labs/osmosis/blob/ee48cf581d020f28ed250a9c4c5d13338cdd94c1/docs/core/proto-docs.md#osmosis.gamm.v1beta1.QueryTotalPoolLiquidityResponse
        return [ Coin.from_data(asset) for asset in res['liquidity']]

    


class GAMMAPI(AsyncGAMMAPI):
    @sync_bind(AsyncGAMMAPI.num_pools)
    def num_pools(self, ) -> Dec:
        pass

    @sync_bind(AsyncGAMMAPI.pools)
    def pools(self, params: Optional[APIParams] = None ) -> Dec:
        pass

    @sync_bind(AsyncGAMMAPI.pool_liquidity)
    def pool_liquidity(self, pool_id: int) -> List[Coin]:
        pass

    @sync_bind(AsyncGAMMAPI.pool)
    def pool(self, pool_id: int) -> Pool:
        pass
   


