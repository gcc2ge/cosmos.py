import base64
from pathlib import Path

from cosmos_sdk.client.lcd import LCDClient, PaginationOptions
from cosmos_sdk.core import Coin, Coins
from cosmos_sdk.core.bank import MsgSend
from cosmos_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://bombay-lcd.terra.dev/",
        chain_id="bombay-12",
    )

    result = terra.distribution.rewards("terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v")
    print(result)
    result = terra.distribution.validator_commission(
        "terravaloper19ne0aqltndwxl0n32zyuglp2z8mm3nu0gxpfaw"
    )
    print(result)
    result = terra.distribution.withdraw_address(
        "terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v"
    )
    print(result)
    result = terra.distribution.community_pool()
    print(result)
    result = terra.distribution.parameters()
    print(result)


main()
