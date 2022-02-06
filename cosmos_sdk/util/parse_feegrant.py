from cosmos_sdk.core.feegrant import AllowedMsgAllowance, BasicAllowance, PeriodicAllowance

from .base import create_demux, create_demux_proto

msgs = [BasicAllowance, PeriodicAllowance, AllowedMsgAllowance]

parse_feegrant = create_demux(msgs)
parse_feegrant_proto = create_demux_proto(msgs)
