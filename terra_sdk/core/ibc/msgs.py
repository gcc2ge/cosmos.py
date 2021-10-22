"""IBC module message types."""

from __future__ import annotations

import attr

from terra_sdk.core import AccAddress, Coin
from terra_sdk.core.msg import Msg

__all__ = ["MsgTransfer"]


@attr.s
class MsgTransfer(Msg):
    """Perform an IBC transfer
    https://docs.rs/cosmos-sdk-proto/0.6.3/cosmos_sdk_proto/ibc/applications/transfer/v1/struct.MsgTransfer.html

    Args:
        source_channel (str): the channel by which the packet will be sent
        token (Union[Coin, str, dict]): the tokens to be transferred
        sender (str): the sender address
        receiver (str): the recipient address on the destination chain
        timeout_height (Optional[dict[str, str]]): Timeout height relative to the current block
            height. The timeout is disabled when set to 0.
        timeout_timestamp (Optional[int | str]): Timeout timestamp (in nanoseconds) relative to the
            current block timestamp. The timeout is disabled when set to 0.
    """

    type = "cosmos-sdk/MsgTransfer"
    """"""
    source_port = "transfer"
    """"""

    source_channel: str = attr.ib()
    token: Coin = attr.ib(converter=Coin.parse)  # type: ignore
    sender: AccAddress = attr.ib()
    receiver: AccAddress = attr.ib()
    timeout_timestamp: str = attr.ib(default="0", converter=str)
    timeout_height: str | dict = attr.ib(default="0")

    @classmethod
    def from_data(cls, data: dict) -> MsgTransfer:
        data = data["value"]
        return cls(
            source_channel=data["source_channel"],
            token=Coin.from_data(data["token"]),
            sender=data["sender"],
            receiver=data["receiver"],
            timeout_timestamp=data.get("timeout_timestamp", "0"),
            timeout_height=data.get("timeout_height", "0"),
        )
