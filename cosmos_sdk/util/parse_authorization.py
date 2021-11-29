from cosmos_sdk.core.authz import GenericAuthorization, SendAuthorization

from .base import create_demux, create_demux_proto

parse_authorization = create_demux([GenericAuthorization, SendAuthorization])

parse_authorization_proto = create_demux_proto([GenericAuthorization, SendAuthorization])
