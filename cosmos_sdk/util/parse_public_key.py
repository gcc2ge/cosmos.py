from cosmos_sdk.core.public_key import LegacyAminoPubKey, SimplePublicKey, ValConsPubKey

from .base import create_demux, create_demux_proto

msgs = [ValConsPubKey, SimplePublicKey, LegacyAminoPubKey]

parse_pub_key = create_demux(msgs)
parse_pub_key_proto = create_demux_proto(msgs)
