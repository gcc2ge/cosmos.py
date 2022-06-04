from cosmos_sdk.core import Coin, Dec

from .._base import BaseAsyncAPI, sync_bind

from cosmos_sdk.core.gamm import Pool, PoolAsset
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

    async def pool_asset(
        self,
        pool_id: int,
    ) -> List[PoolAsset]:
        res = await self._c._get(f"/osmosis/gamm/v1beta1/pools/{pool_id}/tokens")
        return [ PoolAsset.from_data(asset) for asset in res["poolAssets"]]

    


class GAMMAPI(AsyncGAMMAPI):
    @sync_bind(AsyncGAMMAPI.num_pools)
    def num_pools(self, ) -> Dec:
        pass

    @sync_bind(AsyncGAMMAPI.pools)
    def pools(self, params: Optional[APIParams] = None ) -> Dec:
        pass

    @sync_bind(AsyncGAMMAPI.pool_asset)
    def pool_asset(self, pool_id: int) -> PoolAsset:
        pass

    @sync_bind(AsyncGAMMAPI.pool)
    def pool(self, pool_id: int) -> Pool:
        pass
   


