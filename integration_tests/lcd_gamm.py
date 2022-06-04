from unittest import result
from cosmos_sdk.client.lcd.osmosis.lcdclient import LCDClient
from cosmos_sdk.client.lcd.params import PaginationOptions

def main():
    terra = LCDClient(
        url="https://osmosis.stakesystems.io/",
        chain_id="osmosis-1",
    )

    # pagOpt = PaginationOptions(limit=3,count_total=True)
    # result = terra.gamm.pools(params=pagOpt)
    # print(result)

    # result = terra.gamm.pool_asset(1)
    # print(result)

    result = terra.gamm.pool(1)
    print(result)


main()
