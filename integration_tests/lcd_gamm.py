from unittest import result
from cosmos_sdk.client.lcd.osmosis.lcdclient import LCDClient
from cosmos_sdk.client.lcd.params import PaginationOptions

def main():
    terra = LCDClient(
        url="https://osmosis.stakesystems.io/",
        chain_id="osmosis-1",
    )

    # pagOpt = PaginationOptions(limit=10,key='AAAAAAAAAD0=',count_total=True)
    # result = terra.gamm.pools(params=pagOpt)
    # print(result)

    result = terra.gamm.pool_asset(1)
    print(result)

    # result = terra.gamm.pool(1)
    # print(result.to_data())


main()
