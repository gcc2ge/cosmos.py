from cosmos_sdk.core.distribution.proposals import CommunityPoolSpendProposal
from cosmos_sdk.core.gov.proposals import TextProposal
from cosmos_sdk.core.params.proposals import ParameterChangeProposal
from cosmos_sdk.core.upgrade.data.proposal import CancelSoftwareUpgradeProposal, SoftwareUpgradeProposal

from .base import create_demux, create_demux_proto

msgs = [
    CommunityPoolSpendProposal,
    TextProposal,
    ParameterChangeProposal,
    SoftwareUpgradeProposal,
    CancelSoftwareUpgradeProposal,
]

parse_content = create_demux(msgs)

parse_content_proto = create_demux_proto(msgs)
