from terra_sdk.core.feegrant import BasicAllowance, PeriodicAllowance, AllowedMsgAllowance

from .base import create_demux, create_demux_proto

msgs = [BasicAllowance, PeriodicAllowance, AllowedMsgAllowance]

parse_feegrant = create_demux(msgs)
parse_feegrant_proto = create_demux_proto(msgs)
